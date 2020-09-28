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
from datetime import datetime
# print("Scanning subnet")
#os.system('nmap -sn -oA 127.0.0.0/24 | grep Up  | cut -d " " -f 2 > nmap_test/live-hosts.txt')

connection = UnixSocketConnection()
transform = EtreeTransform()

def get_id(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
        return regexid[0][4:]

name = "cUstome port list"
#print(datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
print(name.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
# #Scanning all ports
# print("Scanning open ports...")
# ipList = ['127.0.0.1', '127.0.0.2', '127.0.0.3', '127.0.0.4']
    # m = re.match('[0-9]+(/tcp)', inhoud)
    # print(m.group(0))
    # for match in re.findall(r'.*(\/tcp)', inhoud):
    print(re.findall(r'.*\/tcp', inhoud))

# cmd = "nmap -p-  " + ' '.join(map(str, ipList)) + " | grep open | cut -d' ' -f1"
# os.system(cmd)
# with open("nmap_test/ports.txt", "r") as f:
#     inhoud = f.read()
#     #Create temp file
#     fh, abs_path = mkstemp()
#     with fdopen(fh,'w') as new_file:
#         new_file.write("T:")
#         for match in re.findall(r'.*\/tcp', inhoud):
#             new_file.write(match[:4]+ ", ")
#         new_file.write("\nU:")
#         for match in re.findall(r'.*\/udp', inhoud):
#             new_file.write(match[:4]+ ", ")
#     #Copy the file permissions from the old file to the new file
#     copymode("nmap_test/ports.txt", abs_path)
#     #Remove original file
#     remove("nmap_test/ports.txt")
#     #Move new file
#     move(abs_path, "nmap_test/ports.txt")

# with Gmp(connection, transform=transform) as gmp:
#     # Login -> change to default admin password
#     gmp.authenticate('scanner', 'scanner')
    
    
#     with open("nmap_test/ports.txt", "r") as f:
#         inhoud2 = f.read()
#     #Creating a new portlist
#     superCooleLijst = gmp.create_port_list('Custome ports123', inhoud2)
#     # mlstr=ElementTree.tostring(superCooleLijst, encoding='utf8', method='xml')
    
#     superCooleLijstID = get_id(superCooleLijst)
#     print(superCooleLijstID)

#     # target=gmp.create_target(target_name, hosts=ipList, port_list_id=)
#     # target_id = get_id(target)

