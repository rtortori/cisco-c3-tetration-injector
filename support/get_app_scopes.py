# Will fetch the list of application scopes

from tetpyclient import RestClient
import json
import requests.packages.urllib3

API_ENDPOINT="https://yourapiendpoint"
CREDENTIALS_FILE='../scripts/tetration_api.json'

requests.packages.urllib3.disable_warnings()
rc = RestClient(API_ENDPOINT, credentials_file=CREDENTIALS_FILE, verify=False)
resp = rc.get('/openapi/v1/app_scopes')

if resp.status_code == 200:
     parsed_resp = json.loads(resp.content)
     print json.dumps(parsed_resp, indent=4, sort_keys=True)
else:
     print resp.status_code
