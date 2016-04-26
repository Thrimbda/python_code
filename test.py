filename = '/media/michael/Macsnow/Route_red.txt'

with open(filename, 'r') as rfobj:
    with open('/media/michael/Macsnow/fmt_red.txt', 'w') as wfobj:
        data = rfobj.readlines()
        for item in data:
            wfobj.write(item.encode().decode("utf-8") + "\n\r")
