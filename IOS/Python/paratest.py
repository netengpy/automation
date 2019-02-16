#!/usr/bin/env python

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# hostname = raw_input("Enter host IP address: ")
# username = raw_input("Enter SSH Username: ")
# password = raw_input("Enter SSH Password: ")

hostname = "1.1.1.1"
username = "cisco"
password = "cisco"


port = 22

ssh.connect(hostname, port, username, password, allow_agent=False, look_for_keys=False)
stdin,stdout,stderr = ssh.exec_command('show ip int bri')

output = stdout.readlines()
print ''.join(output)
ssh.close()