from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree



connection = UnixSocketConnection()
transform = EtreeTransform()

with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
    gmp.authenticate('sam', 'sam')

    reports=gmp.get_reports()
    results=gmp.get_results()
    pretty_print(reports)
    pretty_print(results)