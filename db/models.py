from app import db

class LockedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    file_name = db.Column(db.String(255))
    file_url = db.Column(db.String(255))

    def __init__(self, username, file_name, file_url):
        self.username = username
        self.file_name = file_name
        self.file_url = file_url

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    file_url = db.Column(db.String(255))

    def __init__(self, file_name, file_url):
        self.file_name = file_name
        self.file_url = file_url