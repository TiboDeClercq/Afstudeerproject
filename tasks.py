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
def get_id(inputxml, pre):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<'+ pre + ' id=\"[0-9,a-z,-]*\"',xmlstr.decode('utf8'))
    parsed = []
    [parsed.append(i[5+len(pre):]) for i in regexid] 
    return parsed

#function to get name out of output string when new user/asset is created
def get_name(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<name>[a-z]*</name>',xmlstr.decode('utf8'))
    return regexid

def get_task_list():
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate('thomas', 'Hello!*')
		xml = gmp.get_tasks()
		task_ids = get_id(xml, "task")
		report_ids = get_id(xml, "report")
		map = {}
		for x,y in task_ids,report_ids:
			map[x] = y
		return map

print(get_task_list())
