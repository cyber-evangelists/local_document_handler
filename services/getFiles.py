from flask import jsonify,send_file
import os
def create_file_dict(folder):
    '''
    create files data dictionary

    '''
    file_dict = {} 
    def _list_rec(d, current_path=""):
        if d.isdir():
            for i in d.list():
                new_path = current_path + '/' + i.basename() if current_path else i.basename()
                _list_rec(i, new_path)
        else:
            file_dict[d.basename()] = ['/'+current_path,'_'+current_path.replace('/','_')]

    _list_rec(folder)
    return file_dict



def send_file_to_client(file_path,filename):
    '''
    send file to client
    '''
    try:
        responce = send_file(file_path, as_attachment=True)
        os.remove(filename)
        return 
    except Exception as e:
        return jsonify({"error":f"could not send file to client due to: {e}"}),500