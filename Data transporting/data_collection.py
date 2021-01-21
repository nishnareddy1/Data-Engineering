
import json
import urllib.request

url = "http://rbi.ddns.net/getBreadCrumbData"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode('utf-8'))

with open('bcsample.json', 'w') as writer:
    for i in range(1000):    
        writer.write(str(data[i])+',\n')