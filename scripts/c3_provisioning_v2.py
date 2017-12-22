# Import required modules
import json
import os
from tetpyclient import RestClient
import requests.packages.urllib3

# Configuration file
CONFIG_FILE = './tetinj-configuration.json'

# Declare matching system variables
APP_NAME = os.environ['parentJobName']

# Init vars
API_ENDPOINT=CONFIG_FILE['API_ENDPOINT']
CREDENTIALS_FILE=CONFIG_FILE['CREDENTIALS_FILE']
PARENT_SCOPE = CONFIG_FILE['PARENT_SCOPE']
PARENT_SCOPE_VRF_ID = CONFIG_FILE['PARENT_SCOPE_VRF_ID']
DEFAULT_SCOPE_ID = CONFIG_FILE['DEFAULT_SCOPE_ID']
SENSOR_CONFIG_PROF_ID= CONFIG_FILE['SENSOR_CONFIG_PROF_ID']

APP_SCOPE = '' # This will eventally contain the id of the created object
STATE_FILENAME = './statefile_{}.json'.format(APP_NAME) # This is the name of the file where STATE_DICT will be dumped
STATE_DICT = {} # This dictionary will contain the object created so we can undeploy very easily

# Suppress Insecure Request Warnings
requests.packages.urllib3.disable_warnings()
# Instance rc from Tetration class RestClient
rc = RestClient(API_ENDPOINT, credentials_file=CREDENTIALS_FILE, verify=False)

# Define payload for the creation of the Application Scope on Tetration
scope_req_payload = {
    "short_name": "{}".format(APP_NAME),
    "short_query": {"type":"contains",
        "field": "host_name",
        "value": "{}".format(APP_NAME)
    },
    "parent_app_scope_id": "{}".format(PARENT_SCOPE)
}
scope_resp = rc.post('/openapi/v1/app_scopes', json_body=json.dumps(scope_req_payload))

# Parse the response only if 200OK has been received
if scope_resp.status_code == 200:
     parsed_resp = json.loads(scope_resp.content)
     APP_SCOPE = APP_SCOPE + json.dumps(parsed_resp, indent=4, sort_keys=True)
else:
     print scope_resp.status_code

# Look for the string in the response that contains "id":
for line in APP_SCOPE.splitlines():
    if "\"id\":" in line:
        APP_SCOPE = line.split('"')

# Confirm Application Scope creation
print "Created Application Scope named {} with ID {}".format(APP_NAME,APP_SCOPE[3])
# Add the scope_id of the object we just created into a dictionary that eventually will be dumped in the state file
STATE_DICT["scope_id"] = APP_SCOPE[3]

# Commit dirty scopes
commit_json = {
    'root_app_scope_id': PARENT_SCOPE
}
commit = rc.post('/openapi/v1/app_scopes/commit_dirty', json_body=json.dumps(commit_json))
print "Committed dirty scopes"

# Create an Inventory Filter
APP_SCOPE_ID = APP_SCOPE[3]
INV_FILTER_NAME = "c3_{}_filter".format(APP_NAME) # Change this with your favourite filter format
INV_FILTER_ID = ''

inventory_req_payload = {
   "app_scope_id": DEFAULT_SCOPE_ID,
   "name": "{}".format(INV_FILTER_NAME),
   "query": {
        "field": "host_name",
        "type": "contains",
        "value": "{}".format(APP_NAME)
   }
}

inventory_resp = rc.post('/filters/inventories',
               json_body=json.dumps(inventory_req_payload))

# Parse the response only if 200OK has been received. We are only interested on the Inventory filter ID
if inventory_resp.status_code == 200:
     parsed_resp = json.loads(inventory_resp.content)
     INV_FILTER_ID = parsed_resp["id"]
     # Confirm Inventory Filter creation and write to STATE_DICT
     print "Created Inventory Filter named {} with ID {}".format(INV_FILTER_NAME,INV_FILTER_ID)
     STATE_DICT["inventory_filter_id"] = INV_FILTER_ID
else:
     print "Failed with Resp status code:",inventory_resp.status_code

# Create a software sensor intent
soft_sens_intent_req_payload = {
  "inventory_config_profile_id": "{}".format(SENSOR_CONFIG_PROF_ID),
  "inventory_filter_id": "{}".format(INV_FILTER_ID),
  "version": 1
}

soft_sens_intent_resp = rc.post('/openapi/v1/inventory_config/intents', json_body=json.dumps(soft_sens_intent_req_payload))

if soft_sens_intent_resp.status_code == 201:
     parsed_resp = json.loads(soft_sens_intent_resp.content)
else:
     print "Failed with Resp status code:",soft_sens_intent_resp.status_code

# Get software sensor intent ID. As we don't get a response from the intent creation, we look for the intent ID
# that matches the inventory filter we've just created
soft_intent_resp = rc.get('/openapi/v1/inventory_config/intents')

if soft_intent_resp.status_code == 200:
     parsed_resp = json.loads(soft_intent_resp.content)
     for d in parsed_resp:
         if d["inventory_filter_id"] == INV_FILTER_ID:
             INTENT_ID = d["id"]

# Confirm software sensor intent creation and write to STATE_DICT
print "Created Agent Config intent with ID {}".format(INTENT_ID)
STATE_DICT["agent_config_intent_id"] = INTENT_ID

# Put the intent on top of the list
# Fetch intent list

ilist_resp = rc.get('/inventory_config/orders')
order_result_json = json.loads(ilist_resp.content)

# Create the payload
order_result_json['intent_ids'].insert(0,"{}".format(INTENT_ID))

# Post the new list to the server
reorder_resp = rc.post('/inventory_config/orders',
               json_body=json.dumps(order_result_json))

# Create the interface intent

# Get interface intents list, creates an array with all intent dictionaries
ifaceint_resp = rc.get('/openapi/v1/inventory_config/interface_intents')
order_result_json = json.loads(ifaceint_resp.content)

# Add the new intent on top of the list
order_result_json['intents'].insert(0,{
     "inventory_filter_id": "{}".format(INV_FILTER_ID),
     "vrf_id": PARENT_SCOPE_VRF_ID
})

# Post the new ordering back to the server
reord_ifaceint_resp = rc.post('/openapi/v1/inventory_config/interface_intents',
               json_body=json.dumps(order_result_json))


# Create an application workspace
appws_req_payload = {
   "app_scope_id": "{}".format(APP_SCOPE_ID),
   "name": "{}".format(APP_NAME+"_workspace"),
   "description": "Created by Cloudcenter",
   "primary": True
}
appws_resp = rc.post('/openapi/v1/applications',
               json_body=json.dumps(appws_req_payload))

# Parse the response only if 200OK has been received
if appws_resp.status_code == 200:
    parsed_resp = json.loads(appws_resp.content)
    APPWS_ID = parsed_resp["id"]
    print "Created Primary Application Workspace with ID {}".format(APPWS_ID)
    STATE_DICT["application_workspace_id"] = APPWS_ID
else:
    print appws_resp.status_code

# Open the state file for writing and dump the STATE_DICT dictionary in JSON format
with open(STATE_FILENAME, 'w') as f:
     json.dump(STATE_DICT, f, indent=4, sort_keys=True)