from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree
from time import sleep

def scan(target_name, ipList):
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
        regexid=re.findall(r'<name>[a-z]*</name>',xmlstr.decode('utf8'))
        return regexid

    def get_status(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'<status>[a-zA-Z]*',xmlstr.decode('utf8'))
        return regexid[0][8:]
    
    def get_progress(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'<progress>[0-9]*',xmlstr.decode('utf8'))
        return regexid[0][10:]

    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('sam', 'sam')
        
        #check if scanner user already exists
        if any("<name>scanner</name>" in s for s in get_name(gmp.get_users())):
            print("no new user created")
        else:
            #user creation
            user=gmp.create_user('scanner', password='scanner', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
            user_id = get_id(user)
            print(user_id)


        #target creation
        target=gmp.create_target(target_name, hosts=ipList)
        target_id = get_id(target)

        #task creation
        #arguments: target_name, config_id, target_id, scanner_id
        task=gmp.create_task(target_name, 'daba56c8-73ec-11df-a475-002264764cea', target_id, '08b69003-5fc2-4037-a479-93b440211c73')
        task_id = get_id(task)

        #task start
        gmp.start_task(task_id)
        taskxml=gmp.get_task(task_id)
        print("task started succesfully!")
        while get_status(taskxml)=='Requested' or get_status(taskxml)=='Running':
            taskxml=gmp.get_task(task_id)
            print(get_status(taskxml))
            if(get_status(taskxml)=='Running'):
                print(get_progress(taskxml))
            sleep(2)
        print(get_status(taskxml))