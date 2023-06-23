from typing import Union
import json
import pandas as pd 
import requests
import urllib
import os 
from fake_useragent import UserAgent
from requests.exceptions import HTTPError
import sys

def call_request(url) -> Union[HTTPError, dict]:
    user_agent = UserAgent()
    headers={'User-Agent': str(user_agent)}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e

    return response.json()

if __name__== "__main__":
    os.chdir(os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0])
    print(os.getcwd())
    
    while True:
        genre = input("Inserire keyword: ")
        per_page=input("Inserire foto per pagina: ")
        page=input("Inserire pagine: ")
        image_folder_path= os.getcwd()+"\images"
        if not os.path.isdir(image_folder_path):
            os.mkdir(image_folder_path)
        parameter={"query":genre,"per_page":per_page,"page":page}
        query= urllib.parse.urlencode(parameter)
        url=f"https://unsplash.com/napi/search/photos?{query}"
        response=call_request(url)
        f = open("image_list.txt","a")
        if len(response['results'])>0:
            for i in range(len(response['results'])):
                filename = response['results'][i]['urls']['raw'].split('/')[-1].split('?')[0]+".jpg"
                folder_path=os.path.join(image_folder_path,genre)
                if not os.path.isdir(folder_path):
                    os.mkdir(folder_path)
                filepath=os.path.join(folder_path,filename)
                r = requests.get(response['results'][i]['urls']['raw'], allow_redirects=True)
                open(filepath.replace("\\", "/"), 'wb').write(r.content)
                temp={ "Genre":genre, "link":response['results'][i]['urls']['raw']}
                f.write(response['results'][i]['urls']['raw']+"\n")
                print(response['results'][i]['urls']['raw'])
        else:
            print("Non trovato")
