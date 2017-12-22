from tetpyclient import RestClient
import json
import requests.packages.urllib3
import os

requests.packages.urllib3.disable_warnings()

# Configuration file
CONFIG_FILE = './tetinj-configuration.json'

# Fetching state JSON file
STATE_FILENAME = os.environ['STATEFILE']

# Configuration
PARENT_SCOPE = CONFIG_FILE['PARENT_SCOPE']
PARENT_SCOPE_VRF_ID = CONFIG_FILE['PARENT_SCOPE_VRF_ID']
API_ENDPOINT = CONFIG_FILE['API_ENDPOINT']
CREDENTIALS_FILE = CONFIG_FILE['CREDENTIALS_FILE']

# Load state JSON file to retrieve the status in dictionary format
with open(STATE_FILENAME, 'r') as f:
     STATE_DICT = json.load(f)

rc = RestClient(API_ENDPOINT, credentials_file=CREDENTIALS_FILE, verify=False)

# Remove the application workspace
resp = rc.delete('/openapi/v1/applications/{}'.format(STATE_DICT["application_workspace_id"]))
if resp.status_code == 200:
     print "Removed Application workspace with ID {}".format(STATE_DICT["application_workspace_id"])
else:
     print "Failed with Resp status code:",resp.status_code

# Remove Agent Config Intent
resp = rc.delete('/openapi/v1/inventory_config/intents/{}'.format(STATE_DICT["agent_config_intent_id"]))

if resp.status_code == 200:
     print "Removed Agent Config Intent with ID {}".format(STATE_DICT["agent_config_intent_id"])
else:
     print "Failed with Resp status code:",resp.status_code

# Remove Inventory Filter
resp = rc.delete('/openapi/v1/filters/inventories/{}'.format(STATE_DICT["inventory_filter_id"]))

if resp.status_code == 200:
     print "Removed Inventory Filter with ID {}".format(STATE_DICT["inventory_filter_id"])
else:
     print "Failed with Resp status code:",resp.status_code

# Remove Application Scope
resp = rc.delete('/openapi/v1/app_scopes/{}'.format(STATE_DICT["scope_id"]))

if resp.status_code == 200:
     print "Removed Application Scope with ID {}".format(STATE_DICT["scope_id"])
else:
     print "Failed with Resp status code:",resp.status_code

# Commit dirty scopes
commit_json = {
    'root_app_scope_id': PARENT_SCOPE
}
commit = rc.post('/openapi/v1/app_scopes/commit_dirty', json_body=json.dumps(commit_json))
print "Committed dirty scopes"