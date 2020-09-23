from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from gvm.protocols.gmpv9 import CredentialType
from gvm.protocols.gmpv9 import ScannerType
from gvm.protocols.gmpv9 import FilterType
import re
from xml.etree import ElementTree

connection = UnixSocketConnection()
transform = EtreeTransform()

user_input=False

target_ip="172.0.0.1"
host_name="localhost"


if user_input:
    target_ip= input("Target ip: ")
    host_name = input("Device name: ")


def get_id(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
    return regexid[0][4:]

def get_name(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<name>[a-z]*</name>',xmlstr.decode('utf8'))
    return regexid

with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
    gmp.authenticate('thomas', 'Hello!*')
    
    if any("<name>scanner</name>" in s for s in get_name(gmp.get_users())):
        print("no new user created")
    else:
        #user creation
        user=gmp.create_user('scanner', password='scanner', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
        user_id = get_id(user)
        print(user_id)


    #target creation
    target=gmp.create_target(host_name, hosts=[target_ip])
    target_id = get_id(target)

    #task creation
    task=gmp.create_task('test2', 'daba56c8-73ec-11df-a475-002264764cea', target_id, '08b69003-5fc2-4037-a479-93b440211c73')
    task_id = get_id(task)
    
    #task start
    gmp.start_task(task_id)
    print("task started succesfully!")
