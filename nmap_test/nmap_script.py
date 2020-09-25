import os
import sys
import re

# print("Scanning subnet")
# os.system('nmap -sn -oA nmap_test/nmap-subnet 127.0.0.0/24 | grep Up nmap_test/nmap-subnet.gnmap | cut -d " " -f 2 > nmap_test/live-hosts.txt')

# print("Scanning open ports")
# os.system("nmap -p- -oA nmap_test/nmap-ports 127.0.0.1 | grep open | cut -d " " -f1 > nmap_test/ports.txt")

with open("nmap_test/ports.txt", "r") as f:
    inhoud = f.read()
    # m = re.match('[0-9]+(/tcp)', inhoud)
    # print(m.group(0))
    # for match in re.findall(r'.*(\/tcp)', inhoud):
    print(re.findall(r'.*(\/tcp)', inhoud))
