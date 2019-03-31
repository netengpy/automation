import requests # used for HTTP requests
import urllib3 # used by HTTP session
import json # used to parse JSON

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# a list of the hosts we wish to access
hosts = ["nxosv1"]

# For each host we wish to connect to
for host in hosts:
    print "\nAuthenticating with the device . . .\n"
    # Get an authentication token for the device
    url = "https://" + host + "/api/mo/aaaLogin.json"
    # Login data
    data = """
    {
      "aaaUser": {
        "attributes": {
          "name": "ansible",
          "pwd": "ansible"
        }
      }
    }
    """
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}, verify=False)
    # uncomment to see the raw JSON
    # print json.dumps(response.json(), indent=2)

    if response.status_code == requests.codes.ok:
        print "Authentication successful!\n"
    else:
        print "Authentication failed! Please verify login credentials!\n"
        exit(0)

    token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
    print "Authentication Token: " + token + "\n"

    # Enable Interface-Vlan feature on the device
    url = "https://" + host + "/api/mo/sys.json"

    data = """{
      "topSystem": {
        "children": [
          {
            "fmEntity": {
              "children": [
                {
                  "fmInterfaceVlan": {
                    "attributes": {
                      "adminSt": "enabled"
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }"""

    cookie = {'APIC-Cookie': token}
    response = requests.post(url, cookies=cookie, data=data, headers={'Content-Type': 'application/json'}, verify=False)

    if response.status_code == requests.codes.ok:
        print "Interface-VLAN feature enabled successfully on the device!\n"
    else:
        print "ERROR: Could not enable Interface-VLAN feature!\n"
        exit(0)
