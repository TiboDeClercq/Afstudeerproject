import sys
import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import os
#GVM importsfrom gvm.connections import UnixSocketConnection
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from gvm.protocols.gmpv9 import CredentialType
from gvm.protocols.gmpv9 import ScannerType
from gvm.protocols.gmpv9 import FilterType
from xml.etree import ElementTree
# print("Scanning subnet")
#os.system('nmap -sn -oA 127.0.0.0/24 | grep Up  | cut -d " " -f 2 > nmap_test/live-hosts.txt')

connection = UnixSocketConnection()
transform = EtreeTransform()

#Scanning all ports
print("Scanning open ports...")
os.system('nmap -p-  127.0.0.1 | grep open | cut -d" " -f1 > nmap_test/ports.txt')

with open("ports.txt", "r") as f:
    inhoud = f.read()
<<<<<<< HEAD
    # m = re.match('[0-9]+(/tcp)', inhoud)
    # print(m.group(0))
    # for match in re.findall(r'.*(\/tcp)', inhoud):
    print(re.findall(r'.*\/tcp', inhoud))
=======
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        new_file.write("T:")
        for match in re.findall(r'.*\/tcp', inhoud):
            new_file.write(match[:4]+ ", ")
        new_file.write(" U:")
        for match in re.findall(r'.*\/udp', inhoud):
            new_file.write(match[:4]+ ", ")
   #Copy the file permissions from the old file to the new file
    copymode("nmap_test/ports.txt", abs_path)
    #Remove original file
    remove("nmap_test/ports.txt")
    #Move new file
    move(abs_path, "nmap_test/ports.txt")


with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
    gmp.authenticate('scanner', 'scanner')
    
    
    with open("nmap_test/ports.txt", "r") as f:
        inhoud2 = f.read()
    
    gmp.create_port_list('Custome ports123', 'T:5432, 9392,  U:')
    
>>>>>>> 25ec56bc0a17a7106894d9317de4f5d8263c9f8f
