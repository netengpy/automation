import requests
import urllib3
from ansible.plugins.callback import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# a list of the hosts we wish to access
# create an empty host dictionary
# we store the hosts in here and then SSH to each one in turn with the
# associated values used for configuration
host_dict = {}

# first, read in the external host data fields
with open("python_rest_host_data") as f:
    for line in f:
        split_line = line.split(',')
        key = split_line[0]
        val = split_line[1:]
        host_dict[key] = val

# For each host we wish to connect to
for host in host_dict.keys():
    (port, username, password, tenant, vrf_name, vrf_description) = host_dict[host]
    print "\nAuthenticating with the device . . .\n"
    # Get an authentication token for the device
    url = "https://" + host + "/api/aaaLogin.json"
    # Login data
    data = """
    {
      "aaaUser": {
        "attributes": {
          "name": "%s",
          "pwd": "%s"
        }
      }
    }
    """ % (username, password)
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}, verify=False)
    # print json.dumps(response.json(), indent=2)

    if response.status_code == requests.codes.ok:
        print "Authentication successful!\n"
    else:
        print "Authentication failed! Please verify login credentials!\n"
        exit(0)

    token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
    print "Authentication Token: " + token + "\n"

    # Create VRF
    url = "https://" + host + "/api/mo/uni/tn-%s.json" % tenant
    # VRF configuration data
    data = """
        {
          "fvCtx": {
              "attributes": {
                "name": "%s",
                "descr": "%s"                
          }
        }
        """ % (vrf_name, vrf_description.strip('\n'))

    cookie = {'APIC-Cookie': token}
    response = requests.post(url, cookies=cookie, data=data, headers={'Content-Type': 'application/json'}, verify=False)

    if response.status_code == requests.codes.ok:
        print "VRF created successfully!\n"
    else:
        print "VRF creation failed!\n"
        exit(0)
