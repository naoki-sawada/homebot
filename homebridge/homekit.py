import sys
import slackweb
import requests
import json

argvs = sys.argv
url = 'http://localhost:8888'
payload = json.loads(argvs[1])
r = requests.post(url, json=payload)
print(r.text)
