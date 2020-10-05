from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree
from base64 import b64decode


connection = UnixSocketConnection()
transform = EtreeTransform()

user = "scanner"
password = "scanner"

class Task:
	def __init__(self, task_id, report_id, task_name):
		self.task_id = task_id
		self.report_id = report_id
		self.task_name = task_name

#function to get ID out of output string when new user/asset is created
def get_id(inputxml, pre):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'<'+ pre + ' id=\"[0-9,a-z,-]*\"',xmlstr.decode('utf8'))
    parsed = []
    [parsed.append(i[6+len(pre):-1]) for i in regexid] 
    return parsed

#function to get name out of output string when new user/asset is created
def get_name(inputxml):
	xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
	regexid=re.findall(r'<name>[A-Za-z\-\_\/0-9:]*</name>',xmlstr.decode('utf8'))
	substr = []
	for x in regexid:
		y = x[6:]
		substr.append(y[:-7])
	return substr

def get_report_name(inputxml):
	xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
	regexid=re.findall(r'<name>[A-Za-z ]*</name>',xmlstr.decode('utf8'))
	substr = []
	for x in regexid:
		y = x[6:]
		substr.append(y[:-7])
	return substr

def get_task_id_list():
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		xml = gmp.get_tasks()
		task_ids = get_id(xml, "task")
		return task_ids

def get_report_formats():
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		xml = gmp.get_report_formats()
		ids = get_id(xml, "report_format")
		names = get_report_name(xml)
		map = {}
		for i in range(len(ids)):
			map[ids[i]] = names[i]
		return map

def get_task(task_id):
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		task = gmp.get_task(task_id)
		task_name = get_name(task)[1]
		report_id = get_id(task,"report")[0]
		return Task(task_id, report_id, task_name)

def get_task_list(task_id_list):
	tasks = []
	for x in task_id_list:
		tasks.append(get_task(x))
	return tasks

def get_data(inputxml):
    xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
    regexid=re.findall(r'</report_format>[a-zA-Z0-9+/=]*',xmlstr.decode('utf8'))
    before = regexid[0][16:]
    return before.encode('utf8')
	
def download_report(report_id, report_format_id):
	with Gmp(connection, transform=transform) as gmp:
		# Login -> change to default admin password
		gmp.authenticate(user, password)   

		base64 = get_data(gmp.get_report(report_id=report_id, report_format_id=report_format_id, details=1))

		f = open(report_id + '.csv', 'wb')
		f.write(b64decode(base64))
		f.close()
