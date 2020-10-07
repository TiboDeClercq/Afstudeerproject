from flask import Flask, render_template, request, redirect, url_for, Response, send_file
import socket, threading
import sys, os
from datetime import datetime
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scan import scan, is_requested, is_running, get_newprogress
from questions import questions
import tasks
from setup import set_dhcp, set_static_ip, get_ip, get_subnet
#from .. from setup import set_static_ip, set_dhcp
import re
import asyncio
#import websockets
from zipfile import ZipFile
import json

app = Flask(__name__)

IpAddressen = []
task_list=tasks.get_task_list(tasks.get_task_id_list())
report_format_list = tasks.get_report_formats()
errorList = []
progr=0
task_id_for_progr = " "
temp_deviceName= " "
already_running=False
thread_list=[]

conf_id = "698f691e-7489-11df-9d8c-002264764cea"

#function to check if entered IP address is valid
def valid_ip(address):
    try: 
        socket.inet_aton(address)
        #if the entered IP address is not in the list -> add to list
        if address in IpAddressen:
            errorList.append('This IP address is already in the list.')
        elif re.match(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", address):
            IpAddressen.append(address)
            return True
    except:
        #print("This IP address is not valid.")
        errorList.append('This IP address is not valid.')
        return False

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

@app.route('/createScan', methods=["GET"])
def createScan():
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route("/addIP", methods=["POST"])
def addIP():
    entered_text=request.form.get("inputIP")
    errorList.clear()
    if not entered_text:
        print("You haven't entered an IP address")
    elif valid_ip(entered_text):
        print('Addres succesfully added')
    return render_template('index.html', IpAdressen=IpAddressen, errorList=errorList)

@app.route("/delIP", methods=["POST"])
def delIP():
    entered_text=request.form.get("delIP")
    if IpAddressen:
        print(entered_text)
        IpAddressen.remove(entered_text)
    return render_template('index.html', IpAdressen=IpAddressen)     

@app.route("/delIP", methods=["GET"])
def delIP2():
    return redirect(url_for('index'))

def set_temp_deviceName(newname):
    global temp_deviceName 
    temp_deviceName = newname

def set_already_running(newstatus):
    global already_running 
    already_running = newstatus

@app.route('/sendScan', methods=["POST"])
def sendScan():
    conf_id=request.form.get("conf")
    deviceName= request.form.get("inputName")
    if not deviceName:
        print("You haven't entered a device name.")
        errorList.append("You haven't entered a device name.")
    if not IpAddressen:
        print("You haven't entered any IP address.")
        errorList.append("You haven't entered any IP address.")
    else:
        print("Success")
        #Target has to be unique. Date and time will be added to the devicename.
        targetUniqueName = deviceName.replace(' ', '-').lower() + "_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        if task_id_for_progr == " ":
            task_id= scan(targetUniqueName, IpAddressen, conf_id)
            set_task_id_for_progress(task_id)
            set_temp_deviceName(deviceName)
        else:
            task_id=task_id_for_progr
            deviceName=temp_deviceName
        questions()
        IpAddressen[:]=[]
        return success(task_id, deviceName)

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
    #setter zorgt ervoor dat nieuwe progress en id is opgeslagen
    if is_requested(task_id) or is_running(task_id):
        while(progr != 100):
            if is_requested(task_id) or is_running(task_id):
                set_progress(get_newprogress(task_id))
            else:
                break
        set_task_id_for_progress(" ")
        set_already_running(False)
        set_progress(0)
    else:
        set_task_id_for_progress(" ")
        set_already_running(False)
        set_progress(0)

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

def success(task_id, deviceName):
    #voert progresschack uit zodat progr wordt veranderd
    if already_running == False:
        t1=threading.Thread(target=progress_check, args=(task_id,))
        thread_list.append(t1)
        t1.start()
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
    ip=get_ip()
    subnet=get_subnet()
    print(ip)
    print(subnet)
    return render_template('config.html', ip=ip, subnet=subnet)

@app.route('/staticip', methods=["POST"])
def staticip():
    ip = request.form.get("ip")
    subnet=request.form.get("subnet")
    set_static_ip(ip, subnet)
    return config_GET()

@app.route('/dhcp', methods=["POST"])
def dhcp():
    set_dhcp()
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
@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route('/scan')
def scann():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    app.run(debug=True)   
