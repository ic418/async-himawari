import requests
import re
import json
url = 'https://sc-nc-web.nict.go.jp/wsdb_osndisk/shareDirDownload/bDw2maKV'
login_url='https://sc-nc-web.nict.go.jp/wsdb_osndisk/shareDirDownload/login/bDw2maKV'
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def get_CookieToken():
    dic={}
    s=requests.session()
    response = s.get(url,headers=headers)
    response=s.get(login_url,headers=headers,cookies=requests.utils.dict_from_cookiejar((s.cookies)))
    match = re.search('var FIXED_TOKEN = "(.*)";', response.text)

    dic['CAKEPHP']=requests.utils.dict_from_cookiejar((s.cookies))['CAKEPHP']
    match = re.search('var FIXED_TOKEN = "(.*)";', response.text)
    if match:
        value = match.group(1)
        dic['FIXED_TOKEN']=value
    else:
        print("没有找到FIXED_TOKEN")
        return
    
    

    return dic

def update_CookieToken(filename='./Tokie/cookie_token.json'):
    cookie_dict=get_CookieToken()
    with open(filename, 'w') as json_file:
        json.dump(cookie_dict, json_file)

def read_CookieToken(filename='./Tokie/cookie_token.json'):
    with open(filename, 'r') as json_file:
        return json.load(json_file)


if __name__ == "__main__":

    print((get_CookieToken()))
