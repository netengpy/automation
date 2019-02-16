device_list = []
f = open('device_list.txt', 'r')
for line in f:
    device_list.append(line.strip())
f.close()
print device_list