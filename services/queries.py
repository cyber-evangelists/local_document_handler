from db.models import LockedFile
from app import db
def insert_locked_file(username,filename,path):
    new_locked_file = LockedFile(username=username, file_name=filename, file_url=path)
    db.session.add(new_locked_file)
    db.session.commit()



def delete_locked_file(username,filename,file_path):
    file_path = '/'+file_path
    deleted_count = (
        db.session.query(LockedFile)
        .filter_by(username=username, file_name=filename, file_url=file_path)
        .delete()
    )

    db.session.commit()


def check_record_exists(file_name,path):
    result = LockedFile.query.filter_by(file_name=file_name, file_url=path).first()
    print('check in check record exist:',result)
    if result:
        return True
    else:
        return False
    
def check_record_exists_against_user(username,file_name,path):
    result = LockedFile.query.filter_by(file_name=file_name, file_url='/'+path,username=username).first()
    if result.username==username:
        return True
    else:
        return False


def check_same_user(username,file_name,file_path):
    result = LockedFile.query.filter_by(file_name=file_name, file_url=file_path,username=username).first()
    if result.username==username:
        return True
    else:
        return False