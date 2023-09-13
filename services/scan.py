import hashlib
from virus_total_apis import PublicApi
from dotenv import load_dotenv
load_dotenv()
import os
def scanner(filename):
    API_KEY = os.getenv("SCANAPI")
    with open(filename, "rb") as file:
        EICAR_MD5 = hashlib.md5(file.read()).hexdigest()

    vt = PublicApi(API_KEY)
    response = vt.get_file_report(EICAR_MD5)
   
    if response["response_code"] == 200:
        return response["results"]["response_code"] == 0 or response["results"]["positives"] == 0
    return False