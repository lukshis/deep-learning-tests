import requests
import json
import os.path as path

print("--Start downloadData.py--")

url = "https://vrlab.lt/hands_ml/dataset/files.php"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)

print("--Requesting data--")

data = json.loads(response.content.decode())

print("--Loaded JSON--")

for file in data:
    file_path = "./data/" + file
    if not path.exists(file_path):
        url_file = "https://vrlab.lt/hands_ml/dataset/{}".format(file)
        file_response = requests.get(url_file, headers=headers)
        open(file_path, "w").write(file_response.content.decode())

print("--Download Completed--")