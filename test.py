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
    # Retrieve GMP version supported by the remote daemon
    version = gmp.get_version()

    # Prints the XML in beautiful form
    pretty_print(version)

    # Login
    gmp.authenticate('sam', 'sam')
    
   # gmp.create_credential(
   # name='sam',
   # credential_type=CredentialType.USERNAME_PASSWORD,
   # login='sam',
   # password='sam',
   # )
#    pretty_print(gmp.get_users())
    #user_id='21f4cb59-262f-473a-8cc8-1876f1ed84a2'
#    user_id='84313db1-e8d8-4d61-a100-e521d3ee956f'
#    scanner_id='e2b8f5a5-e662-4d13-a69e-f5c8115f5280'
    #pretty_print(gmp.get_credentials())
    #pretty_print(gmp.get_scanners())

    # Retrieve all tasks
#    tasks = gmp.get_tasks()

    # Get names of tasks
 #   task_names = tasks.xpath('task/name/text()')
    #pretty_print(task_names)

 #    host=gmp.create_host('test')
 #   pretty_print(host)

 #   scanner=gmp.create_scanner('testscanner', 'test', 22, ScannerType.GMP_SCANNER_TYPE,user_id)
 #   pretty_print(scanner)

    #pretty_print(gmp.get_configs())
    #pretty_print(gmp.get_targets())
#    task=gmp.create_task('testtask', 'daba56c8-73ec-11df-a475-002264764cea', '858c93d3-e17a-4662-b6fd-4e820adc1971','e2b8f5a5-e662-4d13-a69e-f5c8115f5280') 
#    pretty_print(task)
#    pretty_print(gmp.get_roles())
    user=gmp.create_user('plop', password='plop', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
    xmlstr=ElementTree.tostring(user, encoding='utf8', method='xml')
    print(xmlstr)
    
    user_id=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
    user_idd=user_id[5:]
    pretty_print(user_id)
    pretty_print(user_idd)









