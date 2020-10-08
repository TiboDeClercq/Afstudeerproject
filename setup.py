import subprocess
import os
import re

def get_interface():
    os.system("ip a > interfaces.txt")
    with open ("interfaces.txt", "r") as f:
        interfaces = re.findall(r'[0-9]*:\s[a-z]*[0-9]*[a-z]*[0-9]*:\s.*UP', f.read())
        interfaces = re.findall(r'[0-9]*:\s[a-z]*[0-9]*[a-z]*[0-9]*', interfaces[1])
        interface = interfaces[0][3:]
        return interface

def set_static_ip(address, netmask):
    if address =="" or netmask=="":
        print("niks aanwezig")
    else:      
        interface = get_interface()
        print(address)
        print(netmask)
        os.system("sudo ifconfig " + str(interface) + " " + str(address) + " netmask " + str(netmask))
        print("static_ip_set")
        

def set_dhcp():
    interface = get_interface()
    os.system("sudo dhclient " + interface + " -v")
    print("dhcp set")

