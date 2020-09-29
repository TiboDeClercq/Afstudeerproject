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
import os

import time
from console_progressbar import ProgressBar
from tqdm import tqdm

import questions

def scan(target_name, ipList, config_id):
    thread_list=[]
    connection = UnixSocketConnection()
    transform = EtreeTransform()

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

    def get_status(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'<status>[a-zA-Z]*',xmlstr.decode('utf8'))
        return regexid[0][8:]
    
    def get_progress(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'<progress>[0-9]*',xmlstr.decode('utf8'))
        return regexid[0][10:]

    def progressbar(taskid):
            print("thread started")
            taskxml=gmp.get_task(taskid)
            print(get_name_without(taskxml),": ", get_status(taskxml))
            #print(get_name_without(taskxml),": ", "0 %")
            #progr = 0
            #pb = ProgressBar(total = 100, decimals=0, length=50, fill='=', zfill=' ')
            i = 0
            pbar = tqdm(total = 100, initial = i)
            while (get_status(taskxml)=='Requested' or get_status(taskxml)=='Running'):
                taskxml=gmp.get_task(taskid)
                #if(get_status(taskxml)=='Running'):
                    #for i in tqdm (range (100), desc=get_name_without(taskxml)):
                while(get_status(taskxml)=='Running' and i < int(get_progress(taskxml))):
                    if(get_progress(taskxml) != ''):
                        oldi = i
                        i = int(get_progress(taskxml))
                        pbar.update(i - oldi)
            # while get_status(taskxml)=='Requested' or get_status(taskxml)=='Running':
            #     taskxml=gmp.get_task(taskid)
            #     if(get_status(taskxml)=='Running' and progr < int(get_progress(taskxml))):
            #         print("\n", get_name_without(taskxml),": ")
            #         pb.print_progress_bar(int(get_progress(taskxml)))
            #     if(get_progress(taskxml) != ''):
            #         progr = int(get_progress(taskxml))
            print(get_status(taskxml))

    def custome_port_table():
        #Scanning all ports
        print("Scanning open ports...")
        # os.system('nmap -p-  127.0.0.1 | grep open | cut -d" " -f1 > nmap_test/ports.txt')
        #Commando dat de scan gaat uitvoeren voor al de ip addressen 
        cmd = "nmap -p-  " + ' '.join(map(str, ipList)) + " | grep open | cut -d' ' -f1 > ports.txt"
        os.system(cmd)

        with open("ports.txt", "r") as f:
            inhoud = f.read()
            print(inhoud)
            #Create temp file
            fh, abs_path = mkstemp()
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
            copymode("ports.txt", abs_path)
            #Remove original file
            remove("ports.txt")
            #Move new file
            move(abs_path, "ports.txt")

    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        #gmp.authenticate('sam', 'sam')
        gmp.authenticate('scanner', 'scanner')

        #check if scanner user already exists
        if any("<name>scanner</name>" in s for s in get_name(gmp.get_users())):
            print("no new user created")
        else:
            #user creation
            user=gmp.create_user('scanner', password='scanner', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
            user_id = get_id(user)
            print(user_id)

        gmp.authenticate('scanner', 'scanner')
        # #target creation
        #target=gmp.create_target(target_name, hosts=ipList)
        #target_id = get_id(target)
        custome_port_table()
        #target creation with custome port list
        with open("ports.txt", "r") as f:
            inhoud2 = f.read()
            print(inhoud2)
        #Creating a new portlist
        portListName = target_name.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        print(portListName)
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
        
        print("task started succesfully!")
        t1=threading.Thread(target=progressbar, args=(task_id,))
        thread_list.append(t1)
        t1.start()
    