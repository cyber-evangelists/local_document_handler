from app import mysql

def insert_locked_file(username,filename):
    cur = mysql.connection.cursor()
    insert_query = "INSERT INTO locked_files (username, file_name, file_url) VALUES (%s, %s, %s)"
    data = (username, filename, '/'+filename)
    cur.execute(insert_query, data)
    mysql.connection.commit()
    cur.close()

def save_logs_in_db(username,machine,descriptoion,filename):
    cur = mysql.connection.cursor()
    insert_query = "INSERT INTO Logging (Description, UserName, Machine,Filename) VALUES (%s, %s, %s, %s)"
    data = (descriptoion, username, machine, filename)
    cur.execute(insert_query, data)
    mysql.connection.commit()
    cur.close()

def get_logs_from_db(username,machine,filename):
    cur = mysql.connection.cursor()
    select_query = """
            SELECT Description
            FROM Logging
            WHERE UserName = %s
              AND Machine = %s
              AND filename = %s
            ORDER BY created_at DESC
            LIMIT 1;
        """
    data = (username, machine, filename)
    cur.execute(select_query, data)
    result = cur.fetchone()
    cur.close()
    if result:
        return result[0]
    else:
        return None

def delete_locked_file(username,filename):
    cur = mysql.connection.cursor()
    delete_query = "DELETE FROM locked_files WHERE username = %s AND file_name = %s"
    data = (username, filename)
    cur.execute(delete_query, data)
    mysql.connection.commit()
    cur.close()

def check_record_exists(file_name,path):
    cur = mysql.connection.cursor()
    query = "SELECT id FROM locked_files WHERE file_name = %s AND file_url = %s"
    data = (file_name, path)
    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()
    if result:
        return True
    else:
        return False


def check_same_user(username,file_name,file_path):
    cur = mysql.connection.cursor()
    query = "SELECT username FROM locked_files WHERE file_name = %s AND file_url = %s"
    data = (file_name, file_path)
    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()
    if result[0]==username:
        return True
    else:
        return False