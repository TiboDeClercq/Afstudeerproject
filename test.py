from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree
from base64 import b64decode



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

def get_pdf(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'</report_format>[a-zA-Z0-9+/=]*',xmlstr.decode('utf8'))
    before = regexid[0][16:]
    return before.encode('utf8')

with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
    gmp.authenticate('thomas', 'Hello!*')
    
    #get report as pdf
    base64 = get_pdf(gmp.get_report("ee818589-db5d-40d2-a1a6-55a7aedfb535", report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5"))

    bytes = b64decode(base64, validate=True)
    if bytes:
        f = open('report.pdf', 'wb')
        f.write(base64)
        f.close()

    