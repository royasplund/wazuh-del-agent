#!/usr/bin/env python3

import json
import requests
import urllib3
from base64 import b64encode

# Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
protocol = 'https'
host = ''
port = 55000
user = ''
password = ''
login_endpoint = 'security/user/authenticate'
agent_id = ''

login_url = f"{protocol}://{host}:{port}/{login_endpoint}"
basic_auth = f"{user}:{password}".encode()
login_headers = {'Content-Type': 'application/json',
                 'Authorization': f'Basic {b64encode(basic_auth).decode()}'}


response = requests.post(login_url, headers=login_headers, verify=False)
print(f"\nTOKEN DATA: {response.text}\n\n")
token = json.loads(response.content.decode())['data']['token']


requests_headers = {'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'}


print("Attempting to delete agent\n")

#REQUEST TO LIST AGENTS
#response = requests.get(f"{protocol}://{host}:{port}/agents?pretty=true&older_than=21d&agents_list=all&status=never_connected,disconnected", headers=requests_headers, verify=False)
#print(response.text)

#REQUEST TO DELETE AGENTS
response = requests.delete(f"{protocol}://{host}:{port}/agents?pretty=true&older_than=0s&agents_list={agent_id}&status=all", headers=requests_headers, verify=False)
message = response.text

if '"error": 1' in message:
    parsed = message.split('\n', -1)
    test = list(filter(lambda msg: 'message' in msg, parsed))
    print(f"ERROR: {test}")
else:
    print("Agent was deleted")
