import paramiko
import time

# a list of the hosts we wish to access
hosts = ["apic"]

# NXOS login details
username = "admin"
password = "C1sco12345"

# Create a new Paramiko SSH connection object
conn = paramiko.SSHClient()
# Automatically add SSH hosts keys
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# For each host we wish to connect to
for host in hosts:
        print "--------------------",host,"--------------------"
        # create a shell session for multiple commands
        conn.connect(host, 22, username, password, look_for_keys=False, allow_agent=False)
        remote_shell = conn.invoke_shell()
        # receive remote host shell output
        output = remote_shell.recv(65535)
        # display the output
        print output

        # send the command "configure terminal"
        remote_shell.send("configure terminal\n")
        time.sleep(.5)
        output = remote_shell.recv(65535)
        print output

        # Create a tenant
        remote_shell.send("tenant ACILab_clitest\n")
        time.sleep(.5)
        output = remote_shell.recv(65535)
        print output

        # set description for the tenant
        remote_shell.send("description 'A sample tenant'\n")
        time.sleep(.5)
        output = remote_shell.recv(65535)
        print output

        # exit the configuration mode
        remote_shell.send("end\n")
        time.sleep(.5)
        output = remote_shell.recv(65535)
        print output
        time.sleep(.5)

        # close the SSH session to this host we can re-use the object for the
        # next host
        conn.close()

