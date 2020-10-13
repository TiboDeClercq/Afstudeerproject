from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import re
from xml.etree import ElementTree
from base64 import b64decode
import os
from zipfile import ZipFile
from configparser import ConfigParser

connection = UnixSocketConnection()
transform = EtreeTransform()

user = "scanner"
password = "scanner"

class Task:
	def __init__(self, task_id, report_id, task_name):
		self.task_id = task_id
		self.report_id = report_id
		self.task_name = task_name

def create_default_user():
    with Gmp(connection, transform=transform) as gmp:
    # Login -> change to default admin password
        gmp.authenticate('admin', '444c6ee8-f3f9-4bd8-873a-bbfdf37b8221')
        #check if scanner user already exists
        if any("<name>scanner</name>" in s for s in get_name(gmp.get_users())):
            print("no new user created")
        else:
            #user creation
            user=gmp.create_user('scanner', password='scanner', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
	
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

def get_target_name(inputxml):
	xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
	regexid=re.findall(r'\<target id="[0-9a-z-]*',xmlstr.decode('utf8'))
	target_id=regexid[0][:12]
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		result=gmp.get_target(target_id)
		pretty_print(result)
	return regexid[0][:12]

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
		for i in 0,4,6:
			map[ids[i]] = names[i]
		return map

def get_task(task_id):
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		task = gmp.get_task(task_id)
		task_name = get_name(task)[1]
		#get_target_name(task)
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
	formats = get_report_formats()
	try:
		os.system("mkdir reportdownload")
	except:
		print("directory exists")
	with Gmp(connection, transform=transform) as gmp:
		# Login -> change to default admin password
		gmp.authenticate(user, password)   

		base64 = get_data(gmp.get_report(report_id=report_id, report_format_id=report_format_id, details=1))

		f = open("reportdownload/" + report_id + '.csv', 'wb')
		f.write(b64decode(base64))
		f.close()

def zip_files(report_id):
	config=ConfigParser()
	config.read("config.ini")
	report_format=config["REPORT"]

	download_report(report_id, report_format["id"])
	full_target_name=get_target_name(report_id)
	target_name=get_target_name(report_id)[:-20]
	path = "txtfiles/answers_target_" + target_name
	reportpath = "reportdownload/" + report_id + ".csv"
	answerpath="answers.txt"

	try:
		os.system("mkdir zipfiles")
	except:
		print("directory exists")

	zipObj = ZipFile("zipfiles/"+target_name+'.zip', 'w')
	try:
		zipObj.write(path)
	except:
		print("path to portquestions does not exist")
	
	try:
		zipObj.write(reportpath)
	except:
		print("path to report does not exist")
	
	try:
		zipObj.write(answerpath)
	except:
		print("path to answers general questions does not exist")
	zipObj.close()
	print("successfull zipped")

def get_target_name(report_id):
	with Gmp(connection, transform=transform) as gmp:
		gmp.authenticate(user, password)
		xml = gmp.get_report(report_id)
		l = get_name(xml)
		return l[-1]
