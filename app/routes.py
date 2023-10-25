from app import app
from flask import request, jsonify, send_file
from services.getFiles import create_file_dict
from services.queries import (
    insert_locked_file,
    delete_locked_file,
    check_record_exists,
    check_same_user,
    check_record_exists_against_user
)
from services.scan import scanner
from nextcloud import NextCloud
from services.logs import logger
from pathvalidate import sanitize_filename, sanitize_filepath
from services.cryptograph import encrypt_value, decrypt_value
from dotenv import load_dotenv
load_dotenv()
import os
root_dir = os.getcwd()
NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')




@app.route('/get_files_data',methods=['POST'])
def get_files_name():
    '''
    get username and password from request body
    get files data from nextcloud
    create file dictionary
    return file dictionary

    '''
    try:
        json_data = request.json
        username = decrypt_value(json_data.get('username'))
        password = decrypt_value(json_data.get('password'))
        if username is None or password is None:
            logger.error('username or password is missing')
            return jsonify({"status":"username or password is missing"}),404
        
        nxc = NextCloud(endpoint = NEXTCLOUD_URL, user=username, password=password)

        root = nxc.get_folder() 
        file_dict = create_file_dict(root)
        del file_dict['checklogin.txt']
        return file_dict, 200
    except Exception as e:
        logger.error(f"could not get file details due to: {e}")
        return jsonify({"status":f"could not get file details due to: {e}"}),500
    


@app.route('/get_file',methods=['POST'])
def get_file():
    '''
    get username,filename, file path and password from request body
    check if file exists in nextcloud
    check if file is locked by another user
    if not locked by another user
        download file
        scan file
        return file
    else
        return error
    '''
    file_name_to_remove = None
    try:
        json_data = request.json
        username = decrypt_value(json_data.get('username'))
        password = decrypt_value(json_data.get('password'))
        if username == False or password == False:
            logger.error('invalid username or password!')
            return jsonify({'status':'invalid username or password!'}),403
        filename = sanitize_filename(json_data.get('file_name'))
        file_path = sanitize_filepath(json_data.get('file_path'))
        if filename is None or username is None or password is None or file_path is None:
            logger.error('filename or username or password is missing or file_path is missing')
            return jsonify({'status':'filename or username or password is missing or file_path is missing'}),404
        
        nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password)
        file = nxc.get_file(file_path)
        if file is not None:
            file.fetch_file_content()
            file.download()
            current_file_path = os.path.join(root_dir, filename)
            file_name_to_remove = filename
            if not check_record_exists(filename,file_path):
                insert_locked_file(username,filename,file_path)
                if scanner(filename):
                    response = send_file(current_file_path, as_attachment=True)
                    os.remove(filename)
                    logger.info('file downloaded successfully')
                    return response,200
                else:
                    os.remove(filename)
                    logger.error('file has virus')
                    return jsonify({'status':'file has virus'}),500
                
            elif check_same_user(username,filename,file_path):
                if scanner(filename):
                    response = send_file(current_file_path, as_attachment=True)
                    os.remove(filename)
                    logger.info('file downloaded successfully')
                    return response
                else:
                    os.remove(filename)
                    logger.error('file has virus')
                    return jsonify({'status':'file has virus'}),500
            else:
                os.remove(filename)
                return jsonify({'status':'file already in editing process by another user'}),409
            
        else:
            logger.warning('file not exist or user have not access')
        return jsonify({'status':'file not exist or user have not access'}),404
    except Exception as e:
        logger.error(f'could not get file due to the: {e}')
        if file_name_to_remove:
            os.remove(file_name_to_remove)
        return jsonify({'status':f'could not get file due to the: {e}'}),500

@app.route('/upload_file',methods=['POST'])
def upload_file():
    '''
    get username,filename, file and password from request body
    scan file
    upload file to nextcloud
    return success or error
    '''
    file_name_to_remove = None
    try:
        check = None
        username = request.form.get('username')
        password = request.form.get('password')
        file_path = sanitize_filepath(request.form.get('file_path'))
        if 'file' not in request.files:
            logger.error('No file in request')
            return jsonify({'status':'No file part'}),404
        nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password)
        file = request.files['file']
        file.save(file.filename)
        file_name_to_remove = file.filename
        # if check_record_exists_against_user(username,file.filename,file_path):
        if nxc:
            delete_locked_file(username,file.filename,file_path)
            if scanner(file.filename):
                check = nxc.upload_file(file.filename, file_path).data
                os.remove(file.filename)
                if check=='':
                    logger.info('file uploaded successfully')
                    return jsonify({'Messege':'file uploaded successfully'}),200
                else:
                    logger.error(f'file upload failed:{check}')
                    return jsonify({'status':f'file upload failed:{check}'}),500
            else:
                os.remove(file.filename)
                logger.error('file has virus')
                return jsonify({'status':'file has virus'}),500
        elif check_record_exists(username,file.filename,file_path):
            os.remove(file.filename)
            logger.error('file is being edited by other user.')
            return jsonify({'status':'file is being edited by other user'}),500
        else:
            os.remove(file.filename)
            logger.error('file operation failed.')
        return jsonify({'status':'file operation failed'}),500
        
    except Exception as error:
        logger.error(f'could not upload file due to:{error}')
        if file_name_to_remove:
            os.remove(file_name_to_remove)
        return jsonify({'status':f'could not upload file due to:{error}'}),500
    


@app.route('/login',methods=['POST'])
def login():
    '''
    get username and password from request body
    check login
    return success or error

    '''
    try:
        json_data = request.json
        username = json_data.get('username')
        password = json_data.get('password')
        logger.info("f{username}")
        if username is None or password is None:
            logger.error('username or password is missing')
            return jsonify({'status':'username or password or machine is missing or ip is missing'}),404
        nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password)
        check = nxc.upload_file('checklogin.txt', '/flask/checklogin.txt').data
        if check=='':
            return jsonify({
            'status':'login sucessfull',
            'username':encrypt_value(username),
            'password':encrypt_value(password),
            }),200
        else:
            logger.error('login failed from next cloud server')
        return jsonify({'status':'login failed from next cloud'}),401
    except Exception as e:
        logger.error(f'login failed due to: {e}')
        return jsonify({'status':f'login failed:{e}'}),500
