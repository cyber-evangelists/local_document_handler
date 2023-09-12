import hashlib
from virus_total_apis import PublicApi

def scanner(filename):
    API_KEY = '88858f77a2c07a9d4e9b6b730ea378d1d2c02e3c9e3e9ff885cb1e50da23014b'
    with open(filename, "rb") as file:
        EICAR_MD5 = hashlib.md5(file.read()).hexdigest()

    vt = PublicApi(API_KEY)
    response = vt.get_file_report(EICAR_MD5)
   
    if response["response_code"] == 200:
        return response["results"]["response_code"] == 0 or response["results"]["positives"] == 0
    return False