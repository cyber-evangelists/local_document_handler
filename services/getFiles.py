def create_file_dict(folder):
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