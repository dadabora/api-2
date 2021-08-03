import json
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
}
url = 'https://api.github.com/users'
user = 'dadabora'
jsonic = requests.get(f'{url}/{user}/repos').json()

js = {}
for i in range(0, len(jsonic)):
  print("Project Number:", i+1)
  print("Project Name:", jsonic[i]['name'])
  print("Project URL:", jsonic[i]['svn_url'], "\n")
  js[i+1] = {'Name': jsonic[i]['name'], 'URL': jsonic[i]['svn_url']}

with open('les1_1.json', 'w') as outfile:
    json.dump(js, outfile)

# DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU
# https://api.nasa.gov/planetary/apod? api_key = DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU
import urllib.request
from pprint import pprint

ml = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&page=2&api_key=DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU'


f = requests.get(ml).json()
pprint(f)
for i in f['photos']: print('id', i['id'])
param_id = int(input('id = '))
for o in f['photos']:
    if o['id'] == param_id:
        print(o['img_src'])
        foto = o['img_src']
        img = urllib.request.urlopen(foto).read()
        name = f'{param_id}_foto.jpg'
        with open(name, 'wb') as a:
            a.write(img)
            a.close