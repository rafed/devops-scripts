import requests
import base64
import json

organization = ""
project = ""
url_base = f"https://dev.azure.com/{organization}/{project}/"
url_endpoint = "_apis/distributedtask/variablegroups?api-version=6.0-preview.2"
url = url_base + url_endpoint

PAT = ""

authorization = str(base64.b64encode(bytes(':'+PAT, 'ascii')), 'ascii')

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+ authorization
}

r = requests.get(url, headers=headers)

j = json.loads(r.text)
print(json.dumps(j, indent=2))
