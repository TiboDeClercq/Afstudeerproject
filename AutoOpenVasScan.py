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

with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
    gmp.authenticate('sam', 'sam')
    
    #user creation
    user=gmp.create_user('plop', password='plop', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
    xmlstr=ElementTree.tostring(user, encoding='utf8', method='xml')
    user_id=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
    user_id=user_id[0][4:]
    print(user_id)
     
    #to do: dynamic input (ip-address of target, name of host)
    #target creation
    target=gmp.create_target('localhost', hosts='127.0.0.1')
    xmlstr=ElementTree.tostring(target, encoding='utf8', method='xml')
    target_id=re.findall(r'id=\"[0-9,a-z,-]*', xmlstr.decode('utf8'))
    target_id=target_id[0][4:]
    print(target_id)

    #task creation
    task=gmp.create_task('test2', 'daba56c8-73ec-11df-a475-002264764cea', target_id, '08b69003-5fc2-4037-a479-93b440211c73')
    xmlstr=ElementTree.tostring(task, encoding='utf8', method='xml')
    task_id=re.findall(r'id=\"[0-9,a-z,-]*', xmlstr.decode('utf8'))
    task_id=task_id[0][4:]
    print(task_id)
    
    #task start
    gmp.start_task(task_id)
    









