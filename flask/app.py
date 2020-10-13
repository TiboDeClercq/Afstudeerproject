from flask import Flask, render_template, request, redirect, url_for, Response, send_file
import socket, threading
import sys, os
from datetime import datetime
# makes sure the app.py can find all the python scripts in the directory above 
# and call the functions inside these scripts
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scan import scan, is_requested, is_running, get_newprogress, check_for_logging
from questions import getQuestions, submitAnswers
import tasks
from setup import set_dhcp, set_static_ip, get_ip, get_subnet
from update_code import update_code
from configparser import ConfigParser
#from .. from setup import set_static_ip, set_dhcp
import re
import asyncio
#import websockets
from zipfile import ZipFile
import json
import time

app = Flask(__name__)

IpAddressen = []
#tasks.create_default_user()
task_list=tasks.get_task_list(tasks.get_task_id_list())
report_format_list = tasks.get_report_formats()
errorList = []
progr=0
task_id_for_progr = " "
temp_deviceName= " "
already_running=False
thread_list=[]
active_hosts=[]

conf_id = "698f691e-7489-11df-9d8c-002264764cea"

def create_dailylog():
    todays_logs = datetime.now().strftime("%d-%m-%Y")
    
    # check if the directory for the logs exists and if the logfile for this day exists
    try:
        os.system("mkdir logs")
    except:
        print("directory exists")
    try:
        os.system('touch logs/' + todays_logs + '_APPlogs.txt')
    except:
        print("file exists")


#function to check if entered IP address is valid
def valid_ip(address):
    todays_logs = datetime.now().strftime("%d-%m-%Y")
    create_dailylog()
    with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
        try: 
            socket.inet_aton(address)
            #if the entered IP address is not in the list -> add to list
            # if address in IpAddressen:
            #     errorList.append('This IP address is already in the list.')
            if re.match(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", address):
                return True
        except:
            #print("This IP address is not valid.")
            errorList.append('This IP address is not valid.')
            date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            # open logfile and write to it
            file_object.write("\n"+ date_and_time + ": the IP address you entered is not valid.")
            return False

def add_to_IpList(address):
    todays_logs = datetime.now().strftime("%d-%m-%Y")
    
    create_dailylog()

    # open logsfile and write to it
    with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
        date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        if address in IpAddressen:
            errorList.append('This IP address is already in the list.')
            file_object.write("\n"+ date_and_time + ": IP address: " + address + " is already added.")
        elif valid_ip(address):
            IpAddressen.append(address)
            file_object.write("\n"+ date_and_time + ": IP address: " + address + " is added.")

def zip_files(targetname):
    path="txtfiles/answers_target_"+targetname
    try:
        os.system("mkdir zipfiles")
    except:
        print("directory exists")
    zipObj=ZipFile("zipfiles/"+targetname+'.zip', 'w')

    zipObj.write(path)
    zipObj.close
    print("successfull zipped")

# check the eth0 ip address and subnet for active hosts (nmap scan below)
# they get written into a file and this file gets read
@app.route('/activehosts', methods=["GET"])
def activeHostDetect():
    try:
        os.system("mkdir int")
    except:
        print("directory exists")
    os.system('ip a | grep \'eth0\' | grep \'inet\' | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\' > int/intip.txt')
    os.system('ip a | grep \'eth0\' | grep \'inet\' | grep -oP \'/[0-9][0-9]\' > int/intsubnet.txt')
    with open("int/intip.txt", "r") as ipfile:
        ip= ipfile.read()
    with open("int/intsubnet.txt", "r") as subnetfile:
        subnet= subnetfile.read()
    ipaddress= ip.splitlines()[0] + subnet.splitlines()[0]
    os.system('nmap -sn ' + ipaddress + ' > int/activehostsoutputnmap.txt')
    os.system('cat int/activehostsoutputnmap.txt | grep -o \'[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\' > int/activehosts.txt')
    with open("int/activehosts.txt", "r") as hostsfile:
        active_hosts=hostsfile.readlines()
    return render_template('activehosts.html', scannedip=ipaddress, activehosts=active_hosts)

@app.route('/createScan', methods=["GET"])
def createScan():
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route("/addIP", methods=["POST"])
def addIP():
    entered_text=request.form.get("inputIP")
    errorList.clear()
    if not entered_text:
        print("You haven't entered an IP address")
    elif add_to_IpList(entered_text):
        print('Addres succesfully added')
    
    return render_template('index.html', IpAdressen=IpAddressen, errorList=errorList)

@app.route("/delIP", methods=["POST"])
def delIP():
    entered_text=request.form.get("delIP")
    if IpAddressen:
        print(entered_text)
        IpAddressen.remove(entered_text)

        todays_logs = datetime.now().strftime("%d-%m-%Y")

        # open logfile and write to it
        with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
            date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            file_object.write("\n" + date_and_time + ": IP address: " + entered_text + " is deleted.")

    return render_template('index.html', IpAdressen=IpAddressen)     

@app.route("/delIP", methods=["GET"])
def delIP2():
    return redirect(url_for('index'))

# setter for saving devicename of running scan
def set_temp_deviceName(newname):
    global temp_deviceName 
    temp_deviceName = newname

def set_already_running(newstatus):
    global already_running 
    already_running = newstatus

@app.route('/sendScan', methods=["POST"])
def sendScan():
    config=ConfigParser()
    config.read("config.ini")
    scan_info=config["SCAN"]

    conf_id=scan_info["type"]
    print(conf_id)
    deviceName= request.form.get("inputName")

    todays_logs = datetime.now().strftime("%d-%m-%Y")
    date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

    create_dailylog()
    # Open the log file for this day
    with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
        if not deviceName:
            print("You haven't entered a device name.")
            file_object.write("\n"+ date_and_time + ": you haven't entered a valid device name.")
            errorList.append("You haven't entered a device name.")
        if not IpAddressen:
            print("You haven't entered any IP address.")
            file_object.write("\n"+ date_and_time + ": you haven't entered a valid IP address to the list.")
            errorList.append("You haven't entered any IP address.")
        else:
            print("Success")
            #Target has to be unique. Date and time will be added to the devicename.
            targetUniqueName = deviceName.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

            # Checks if the taskid is empty, if it is the scan can run and the tempdevicename, taskid are set. Also writes to the log file it has started
            # Else you get notified that there is a scan running (tempdevicename), also written to the log file
            if task_id_for_progr == " ":
                task_id= scan(targetUniqueName, IpAddressen, conf_id)
                set_task_id_for_progress(task_id)
                set_temp_deviceName(deviceName)
                file_object.write("\n"+ date_and_time + ": your scan " + targetUniqueName + " has started.")
            else:
                task_id=task_id_for_progr
                deviceName=temp_deviceName
                file_object.write("\n"+ date_and_time + ": your scan " + targetUniqueName + " hasn't started. " + deviceName + " is running.")

            IpAddressen[:]=[]
            return success(task_id, deviceName)

#change progress amount and save
def set_progress(newprogr):
    global progr 
    progr = newprogr

def get_progress():
    global progr
    return progr

def set_task_id_for_progress(newid):
    global task_id_for_progr 
    task_id_for_progr = newid

def get_task_id_for_progress():
    global task_id_for_progr
    return task_id_for_progr

def progress_check(task_id):
    #setter makes sure new id and progress is saved
    if progr == 100:
        set_progress(0)
    if is_requested(task_id) or is_running(task_id):
        while(progr != 100):
            if is_requested(task_id):
                set_progress(0)
            elif is_running(task_id):
                set_progress(get_newprogress(task_id))
            else:
                break
        set_task_id_for_progress(" ")
        set_already_running(False)
        set_progress(100)
    
# progress and taskid get written to this page in json format for the js to read
@app.route('/prgrss', methods=["GET"])
def progress_bar():
    if progr is None:
        data = str(0)
    else:
        data = str(progr)
    jsondata = {
        "progrss": data,
        "taskidforprogrss": task_id_for_progr
    }

    j=json.dumps(jsondata)

    return Response(j, mimetype='application/json')

# this function creates a logfile for each activated scan, it takes the information from the gvmd service
# and writes this to the logfile until a scan stops.
def writelogsscan(task_id, deviceName):
    try:
        os.system("mkdir logs")
    except:
        print("directory exists")
    targetUniqueName = deviceName.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    while check_for_logging(task_id) == False:
        os.system('cat /var/log/gvm/gvmd.log | grep ' + task_id + ' > logs/' + targetUniqueName + '_GVMlogs.txt')
        time.sleep(5)
    todays_logs = datetime.now().strftime("%d-%m-%Y")
    with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
        date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        file_object.write("\n"+ date_and_time + ": your scan " + targetUniqueName + " has stopped.")
    

def success(task_id, deviceName):
    # checks progresscheck, to see if the progress has changed
    # second thread for writing of logs
    # the message that's given with the html page shows if the scan starts or if there is one running
    if already_running == False:
        t1=threading.Thread(target=progress_check, args=(task_id,))
        thread_list.append(t1)
        t1.start()
        t2=threading.Thread(target=writelogsscan, args=(task_id, deviceName))
        thread_list.append(t2)
        t2.start()
        set_already_running(True)
        msg="Success, your scan, " + deviceName + " has started"
    else:
        msg="You already have a scan running, " + deviceName

    return render_template('success.html', targetname=deviceName, message=msg)

#Report methods - reports.html
@app.route('/reports', methods=["GET"])
def reports_GET():
    task_list=tasks.get_task_list(tasks.get_task_id_list())
    report_format_list = tasks.get_report_formats()
    return render_template('reports.html', tasks=task_list, reports=report_format_list)

@app.route('/reports', methods=["POST"])
def reports():
    task_list=tasks.get_task_list(tasks.get_task_id_list())
    report_format_list = tasks.get_report_formats()
    return render_template('reports.html', tasks=task_list, reports=report_format_list)

@app.route('/downloadreport', methods=["POST"])
def downloadreport():
    format = request.form.get("format")
    report_id = request.form.get("report_id")
    tasks.download_report(report_id, format)
    path = "../reportdownload/" + report_id + ".csv"
    return send_file(path)

@app.route('/downloadzip', methods=["POST"])
def downloadzip():
    report_id = request.form.get("report_id")
    tasks.zip_files(report_id)
    path= "../zipfiles/" + tasks.get_target_name(report_id)[:-20] + ".zip"
    return send_file(path)

#Configure IP methods - config.html
@app.route('/configuration', methods=["GET"])
def config_GET():
    staticSucces = False
    dhcpSucces = False
    os.system('ip a | grep \'eth0\' | grep \'inet\' | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\' > int/intip.txt')
    with open("int/intip.txt", "r") as ipfile:
        ip= ipfile.read()
    intname= 'eth0'
    os.system('ip a | grep \'eth0\' | grep \'inet\' | grep -oP \'/[0-9][0-9]\' > int/intsubnet.txt')
    with open("int/intsubnet.txt", "r") as subnetfile:
        subnet= subnetfile.read()

    ip = ip.splitlines()[0]
    subnet = subnet.splitlines()[0]
    return render_template('config.html', ip=ip, subnet=subnet, int_name=intname, staticSucces=staticSucces, dhcpSuccess=dhcpSucces)

def config_GET_static(staticSucces):
    intname= 'eth0'
    ip=get_ip()
    subnet=get_subnet()
    print(ip)
    print(subnet)
    return render_template('config.html', ip=ip, subnet=subnet, int_name=intname, staticSucces=staticSucces, errorList=errorList)

def config_GET_dhcp(dhcpSuccess):
    intname= 'eth0'
    ip=get_ip()
    subnet=get_subnet()
    print(ip)
    print(subnet)
    return render_template('config.html', ip=ip, subnet=subnet, int_name=intname, dhcpSuccess=dhcpSuccess)

@app.route('/staticip', methods=["POST"])
def staticip():
    staticSuccess = False
    ip = request.form.get("ip")
    errorList.clear()
    # IpAddressen.clear()
    create_dailylog()
    todays_logs = datetime.now().strftime("%d-%m-%Y")
    with open("logs/" + todays_logs + "_APPlogs.txt", "a") as file_object:
        date_and_time = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        if not ip:
            print("You haven't entered an IP address")
            file_object.write("\n"+ date_and_time + ": You haven't entered an IP address.")
        elif valid_ip(ip):
            print("Static ip is valid")
            file_object.write("\n"+ date_and_time + ": static IP address: " + ip + " is valid.")
            subnet=request.form.get("subnet").replace(" ", "")
            if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',subnet):
                set_static_ip(ip, subnet)
                staticSuccess = True
            else:
                print("werkt niet he man")
                file_object.write("\n"+ date_and_time + ": invalid subnetmask entered.")    
                errorList.append("Subnetmask is not valid")
    return config_GET_static(staticSuccess)

@app.route('/staticip', methods=["GET"])
def staticip_GET():
    return config_GET()

@app.route('/dhcp', methods=["POST"])
def dhcp():
    set_dhcp()
    dhcpSuccess = True
    return config_GET_dhcp(dhcpSuccess)

@app.route('/dhcp', methods=["GET"])
def dhcp_get():
    return config_GET()


@app.route('/portQuestions', methods=["POST"])
def portQuestions():
    port_list=dict()
    with open("ports/ipList.txt", "r") as i:
        ipListStr=i.read()
        ipList=re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ipListStr)
        for ip in ipList:
            with open("ports/"+ ip + ".txt", "r") as f:
                    port_list_str = f.read()            
                    port_list_str=re.findall(r'[\d]*[^,\sTU:]', port_list_str)
                    port_list[ip]=port_list_str
    targetname=request.form.get("targetname")
    return render_template('questions.html', ports=port_list, targetname=targetname, iplist=ipList)

@app.route('/portAnswers', methods=["POST"])
def portAnswers():
    
    AnswerList=dict() 
    targetname=request.form.get("targetname")
    with open("ports/ipList.txt", "r") as i:
        ipListStr=i.read()
        ipList=re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ipListStr)
        for ip in ipList:
            with open("ports/"+ ip +".txt", "r") as f:
                    AnswerListPorts=dict()
                    port_list = f.read()           
                    port_list=re.findall(r'[\d]*[^,\sTU:]', port_list)
                    print(port_list)
                    for port in port_list:                           
                        yesno=request.form.get("inlineRadioOptions"+ ip + port)
                        explanation=""
                        explanation=request.form.get("textArea"+ ip + port)
                        AnswerListPorts[port]=[yesno, explanation]
                        AnswerList[ip]=AnswerListPorts
    print(AnswerList)
    try:
        os.system("mkdir txtfiles")
    except:
        print("directory exists")

    os.system("touch txtfiles/answers_target_" + targetname)

    with open("txtfiles/answers_target_" + targetname, "w") as a:
        for ip in ipList:
            a.write("ip: " + ip + "\n")
            with open("ports/"+ ip +".txt", "r") as f:
                    port_list = f.read()           
                    port_list=re.findall(r'[\d]*[^,\sTU:]', port_list)
                    for port in port_list:
                        a.write("port: " + port + " yes/no: " + AnswerList[ip][port][0] + ", explanation: " + AnswerList[ip][port][1] + "\n")
                        print(AnswerList[ip][port][0])
            a.write("\n")
        #zip_files(targetname)
    return index()

@app.route('/questionOverview', methods=["GET"])
def questionOverview():
    questions = getQuestions()
    return render_template("questionOverview.html", questions=questions)

# @app.route('/addQuestion', methoods=["GET"])
# def addQuestion_GET():
#     return render_template("addQuestion.html")

@app.route('/submitGeneralQuestions', methods=["POST"])
def submitGeneralQuestions():
    questions= getQuestions()
    Answers=[]
    for question in questions:
        answer=request.form.get("answer"+question)
        Answers.append(answer)
    submitAnswers(Answers)
    return index()
    
@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route('/scan')
def scann():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    #update_code()
    app.run(debug=True)   
