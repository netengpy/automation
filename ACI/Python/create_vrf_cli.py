#!/usr/bin/env python2

import paramiko
import time

# create an empty host dictionary
# we store the hosts in here and then SSH to each one in turn with the
# associated values used for configuration
host_dict = {}

# first, read in the external host data fields
with open("python_cli_host_data") as f:
    for line in f:
        split_line = line.split(',')
        key = split_line[0]
        val = split_line[1:]
        host_dict[key] = val

# now we have a dictionary of hosts and configuration values, we can proceed to
# SSH to the hosts and make the configuration changes

# Create a new Paramiko SSH connection object
conn = paramiko.SSHClient()
# Automatically add SSH hosts keys
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in host_dict.keys():
    (port,username, password, tenant, vrf_name, vrf_description) = host_dict[host]

    print "--------------------",host,"--------------------"
    # create a shell session for multiple commands
    conn.connect(host, int(port), username, password, look_for_keys=False, allow_agent=False)
    remote_shell = conn.invoke_shell()
    time.sleep(1)
    # receive remote host shell output
    output = remote_shell.recv(65535)
    # display the output
    print output

    # send the command "configure terminal"
    remote_shell.send("configure terminal\n")
    time.sleep(1)
    output = remote_shell.recv(65535)
    print output

    # Select tenant
    remote_shell.send("tenant "+ tenant+"\n")
    time.sleep(1)
    output = remote_shell.recv(65535)
    print output

    # Create VRF
    remote_shell.send("vrf context " + vrf_name +"\n")
    time.sleep(1)
    output = remote_shell.recv(65535)
    print output

    # set description for VRF
    remote_shell.send("description '" + vrf_description.strip('\n') + "'\n")
    time.sleep(1)
    output = remote_shell.recv(65535)
    print output

    # exit the configuration mode
    remote_shell.send("end\n")
    time.sleep(1)
    output = remote_shell.recv(65535)
    print output
    time.sleep(1)

    # close the SSH session to this host we can re-use the object for the
    # next host
    conn.close()

