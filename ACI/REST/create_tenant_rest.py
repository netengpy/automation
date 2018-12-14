import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# a list of the hosts we wish to access
hosts = ["apic"]

# For each host we wish to connect to
for host in hosts:
    print "\nAuthenticating with the device . . .\n"
    # Get an authentication token for the device
    url = "https://" + host + "/api/aaaLogin.json"
    # Login data
    data = """
    {
      "aaaUser": {
        "attributes": {
          "name": "admin",
          "pwd": "C1sco12345"
        }
      }
    }
    """
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}, verify=False)
    # print json.dumps(response.json(), indent=2)

    if response.status_code == requests.codes.ok:
        print "Authentication successful!\n"
    else:
        print "Authentication failed! Please verify login credentials!\n"
        exit(0)

    token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
    print "Authentication Token: " + token + "\n"

    # Create tenant
    url = "https://" + host + "/api/mo/uni.json"
    # Tenant configuration data
    data = """
        {
            "fvTenant": {
                "attributes": {
                    "name": "ACILab_apitest",
                    "description": "A test tenant"
                }
            }
        }
    """
    cookie = {'APIC-Cookie': token}
    response = requests.post(url, cookies=cookie, data=data, headers={'Content-Type': 'application/json'}, verify=False)

    if response.status_code == requests.codes.ok:
        print "Tenant created successfully!\n"
    else:
        print "Tenant creation failed!\n"
        exit(0)
