from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree
from time import sleep
import threading

import sys
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from datetime import datetime
from configparser import ConfigParser
import os

import time
from tqdm import tqdm

import questions

#function to get ID out of output string when new user/asset is created
def get_id(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
    return regexid[0][4:]

#function to get name out of output string when new user/asset is created
def get_name(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<name>[a-zA-Z]*</name>',xmlstr.decode('utf8'))
    return regexid

def get_name_without(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<name>[a-zA-Z0-9]*',xmlstr.decode('utf8'))
    return regexid[1][6:]

#function to get status out of output string
def get_status(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<status>[a-zA-Z]*',xmlstr.decode('utf8'))
    return regexid[0][8:]

# gets progressval from task
def get_progress(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<progress>[0-9]*',xmlstr.decode('utf8'))
    return regexid[0][10:]

# makes a connection to gvm and checks the status of the task to return the progress 
# (requested = 0 | running returns the amount is gets from the function above)
def get_newprogress(taskid):
    connection = UnixSocketConnection()
    transform = EtreeTransform()
    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('scanner', 'scanner')
        taskxml=gmp.get_task(taskid)

        if is_requested(taskid):
            return 0

        if is_running(taskid):
            return int(get_progress(taskxml)) 

# check to see if the task is requested
def is_requested(taskid):
    connection = UnixSocketConnection()
    transform = EtreeTransform()
    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('scanner', 'scanner')
        taskxml=gmp.get_task(taskid)
        if get_status(taskxml)=='Requested':
            return True
        return False

# check to see if the task is running
def is_running(taskid):
    connection = UnixSocketConnection()
    transform = EtreeTransform()
    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('scanner', 'scanner')
        taskxml=gmp.get_task(taskid)
        if get_status(taskxml)=='Running':
            return True
        return False

# checks if the task is stopped or done to log the state    
def check_for_logging(taskid):
    connection = UnixSocketConnection()
    transform = EtreeTransform()
    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('scanner', 'scanner')
        taskxml=gmp.get_task(taskid)
        if get_status(taskxml)=='Stopped' or get_status(taskxml)=='Done':
            return True
        return False

# was for the cli app, creates a dynamic progress bar in cli and updates this (not used for web interface)
def progressbar(taskid):
        taskxml=gmp.get_task(taskid)
        i = 0
        pbar = tqdm(total = 100, initial = i)
        while (get_status(taskxml)=='Requested' or get_status(taskxml)=='Running'):
            taskxml=gmp.get_task(taskid)
            while(get_status(taskxml)=='Running' and i < int(get_progress(taskxml))):
                if(get_progress(taskxml) != ''):
                    oldi = i
                    i = int(get_progress(taskxml))
                    pbar.update(i - oldi)

#function to create a custom port table with ports scanned by NMAP
def custome_port_table(ipList):
    #read config file
    config=ConfigParser()
    config.read("config.ini")
    nmap_info=config["NMAP"]

    try:
        os.system("mkdir ports")
    except:
        print("dir already exists")
    
    try:
        os.system("rm ports/ports.txt")
        os.system("touch ports/ports.txt")
    except:
        print("dir already exists")
    
    #open ports file where all the open ports will be written to
    with open("ports/ports.txt", "w") as f:
        for ip in ipList:
            try:
                os.system("touch ports/"+ ip  + ".txt")
            except:
                print("dir already exists")
            #nmap command to scan every IP in the list, option to decide how aggressive the scan will be can be modified in config.ini file
            cmd = "nmap "+ ip + " -sS -" + nmap_info["scan"] + "| grep open | cut -d' ' -f1> ports/" + ip + ".txt"
            os.system(cmd)
            #for every IP there will be a seperate file with the open ports        
            with open("ports/" +ip+".txt", "r") as p:
                f.write(p.read())
 
    try:
        os.system("touch ports/ipList.txt")
    except:
        print("ipList already exists")
    
    #all the scanned IP's will be written to a seperate file
    with open ("ports/ipList.txt", "r")as f:
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            for ip in ipList:
                new_file.write(ip + "\n")
    copymode("ports/ipList.txt", abs_path)
    remove("ports/ipList.txt")
    move(abs_path, "ports/ipList.txt") 

    for ip in ipList:
        #the goal for this part is to modify the files so that that a custom port list can be created
        with open("ports/" + ip + ".txt", "r") as f:
            #Create temp file
            inhoud=f.read()
            fh, abs_path = mkstemp()
            # file must have the structure of:
            # T: 22,443, ...
            # U: 80, ...
            with fdopen(fh,'w') as new_file:             
                    new_file.write("T:")
                    for match in re.findall(r'.*\/tcp', inhoud):
                        l=re.findall(r'[\d]*', match)
                        new_file.write(l[0]+ ", ")
                    new_file.write("\nU:")
                    for match in re.findall(r'.*\/udp', inhoud):
                        l=re.findall(r'[\d]*', match)
                        new_file.write(l[0]+ ", ")
        #Copy the file permissions from the old file to the new file
        copymode("ports/" +ip + ".txt", abs_path)
        #Remove original file
        remove("ports/" +ip + ".txt")
        #Move new file
        move(abs_path, "ports/" +ip + ".txt")

    with open("ports/ports.txt", "r") as f:
        inhoud = f.read()
        #Create temp file
        fh, abs_path = mkstemp()
        # file must have the structure of:
        # T: 22,443, ...
        # U: 80, ...
        with fdopen(fh,'w') as new_file:             
                new_file.write("T:")
                for match in re.findall(r'.*\/tcp', inhoud):
                    l=re.findall(r'[\d]*', match)
                    new_file.write(l[0]+ ", ")
                new_file.write("\nU:")
                for match in re.findall(r'.*\/udp', inhoud):
                    l=re.findall(r'[\d]*', match)
                    new_file.write(l[0]+ ", ")
    copymode("ports/ports.txt", abs_path)
    #Remove original file
    remove("ports/ports.txt")
    #Move new file
    move(abs_path, "ports/ports.txt")

def scan(target_name, ipList, config_id):
    thread_list=[]
    connection = UnixSocketConnection()
    transform = EtreeTransform()

    with Gmp(connection, transform=transform) as gmp:
        gmp.authenticate('scanner', 'scanner')

        # #target creation
        custome_port_table(ipList)
        #target creation with custome port list
        with open("ports/ports.txt", "r") as f:
            inhoud2 = f.read()
        #Creating a new portlist
        portListName = target_name.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        superCooleLijst = gmp.create_port_list(portListName, inhoud2)
        pretty_print(superCooleLijst)
        superCooleLijstID = get_id(superCooleLijst)

        target=gmp.create_target(target_name, hosts=ipList, port_list_id=superCooleLijstID)
        target_id = get_id(target)

        # task creation
        # arguments: target_name, config_id, target_id, scanner_id
        task=gmp.create_task(target_name, config_id, target_id, '08b69003-5fc2-4037-a479-93b440211c73')
        task_id = get_id(task)

        #task start
        gmp.start_task(task_id)
        return task_id
        
        print("task started succesfully!")
    
