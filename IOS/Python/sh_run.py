#!/usr/bin/env python

import paramiko
import time
import getpass
import os
import sys
 
#IP = '1.1.1.2'
#USER = raw_input("Username : ")
#PASS = getpass.getpass("Password : ")
#ENABLE = getpass.getpass("Enable : ")

# ONLY FOR TESTING. UNCOMMENT ABOVE AND COMMENT BELOW AFTER TESTING
IP = '1.1.1.2'
USER = 'cisco'
PASS = 'cisco123'
ENABLE = 'cisco123'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IP, port=22, username=USER, password=PASS, look_for_keys=False,allow_agent=False)
remote = ssh.invoke_shell()
remote.send('term len 0\n')

# Un-comment below to send enable command if default priv not 15
#remote.send('enable\n')
#remote.send('%s\n' % ENABLE)
time.sleep(1)

remote.send('sh run\n')
time.sleep(10)

output = remote.recv(65000)
print output

timestr = time.strftime("%Y%m%d-%H%M")

with open('{}-{}.txt'.format(IP, timestr), 'a') as config:
    config.write(output)

ssh.close()
