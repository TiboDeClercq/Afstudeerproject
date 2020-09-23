from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from gvm.protocols.gmpv9 import CredentialType
from gvm.protocols.gmpv9 import ScannerType
from gvm.protocols.gmpv9 import FilterType

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

    credentials='21f4cb59-262f-473a-8cc8-1876f1ed84a2'
    pretty_print(gmp.get_credentials())

    # Retrieve all tasks
    tasks = gmp.get_tasks()

    # Get names of tasks
    task_names = tasks.xpath('task/name/text()')
    pretty_print(task_names)

    host=gmp.create_host('test')
    pretty_print(host)

    scanner=gmp.create_scanner('testscanner', 'test', 22, ScannerType.GMP_SCANNER_TYPE,credentials)
    pretty_print(scanner)
