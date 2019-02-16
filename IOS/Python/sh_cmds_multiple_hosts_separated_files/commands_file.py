host_commands = []
f = open('show_commands.txt', 'r')
for line in f:
    host_commands.append(line.strip())
f.close()
print host_commands