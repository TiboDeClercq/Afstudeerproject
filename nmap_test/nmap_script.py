import sys
import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import os
# print("Scanning subnet")
#os.system('nmap -sn -oA 127.0.0.0/24 | grep Up  | cut -d " " -f 2 > nmap_test/live-hosts.txt')

#Scanning all ports
print("Scanning open ports...")
os.system('nmap -p-  127.0.0.1 | grep open | cut -d" " -f1 > nmap_test/ports.txt')

with open("nmap_test/ports.txt", "r") as f:
    inhoud = f.read()
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        new_file.write("T:")
        for match in re.findall(r'.*\/tcp', inhoud):
            new_file.write(match[:4]+ ", ")
        new_file.write("\nU:")
        for match in re.findall(r'.*\/udp', inhoud):
            new_file.write(match[:4]+ ", ")
        

   #Copy the file permissions from the old file to the new file
    copymode("nmap_test/ports.txt", abs_path)
    #Remove original file
    remove("nmap_test/ports.txt")
    #Move new file
    move(abs_path, "nmap_test/ports.txt")
