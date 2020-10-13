import subprocess
import os
import re


def get_subnet():
    os.system("sudo ifconfig > interfaces.txt")
    with open ("interfaces.txt", "r") as f:
        currentip=re.findall(r'inet \b(?:\d{1,3}\.){3}\d{1,3}\b  netmask \b(?:\d{1,3}\.){3}\d{1,3}\b', f.read())
        currentip=re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', currentip[0])
        currentnetmask=currentip[1]
        return currentnetmask

def get_ip():
    os.system("sudo ifconfig> interfaces.txt")
    with open ("interfaces.txt", "r") as f:
        currentip=re.findall(r'inet \b(?:\d{1,3}\.){3}\d{1,3}\b  netmask \b(?:\d{1,3}\.){3}\d{1,3}\b', f.read())
        currentip=re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', currentip[0])
        currentip=currentip[0]
        return currentip

def get_interface():
    os.system("ip a > interfaces.txt")
    with open ("interfaces.txt", "r") as f:
        interfaces = re.findall(r'[0-9]*:\s[a-z]*[0-9]*[a-z]*[0-9]*:\s.*UP', f.read())
        interfaces = re.findall(r'[0-9]*:\s[a-z]*[0-9]*[a-z]*[0-9]*', interfaces[1])
        interface = interfaces[0][3:]
        return interface

def set_static_ip(address, netmask):
    if address =="" or netmask=="":
        print("empty")
    else:      
        interface = get_interface()
        os.system("sudo ifconfig " + str(interface) + " 0")
        os.system("sudo ifconfig " + str(interface) + " " + str(address) + " netmask " + str(netmask))
        #for cli version (old)
        print("static_ip_set")
        

def set_dhcp():
    interface = get_interface()
    os.system("sudo ifconfig " + str(interface) + " 0")
    os.system("sudo dhclient " + interface + " -v")
    #for cli version (old)
    print("dhcp set")

