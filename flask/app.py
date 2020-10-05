from flask import Flask, render_template, request, redirect, url_for, Response
import socket, threading
import sys, os
from datetime import datetime
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scan import scan, is_requested, is_running, get_newprogress
from questions import questions
import tasks
from setup import set_dhcp, set_static_ip
#from .. from setup import set_static_ip, set_dhcp
import re
import asyncio
import websockets
from zipfile import ZipFile

app = Flask(__name__)

IpAddressen = []
task_list=tasks.get_task_list(tasks.get_task_id_list())
report_format_list = tasks.get_report_formats()
errorList = []
progr=0
oldprogr=0
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
        task_id= scan(targetUniqueName, IpAddressen, conf_id)
        questions()
        IpAddressen[:]=[]
        return success(task_id, deviceName)

#attempt to read print(progress) and store in progr (failed)
# def progrchange(task_id):
#     holder= Object
#     x=0
#     while is_running(task_id):
#         progr=subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[x]
#         x=x+1

def set_progress(newprogr):
    global progr 
    global oldprogr
    oldprogr = progr
    progr = newprogr

def get_progress():
    global progr
    return progr

def progress_check(task_id):
    #setter zorgt ervoor dat nieuwe progress is opgeslagen
    while(progr != 100):
        set_progress(get_newprogress(task_id))

@app.route('/prgrss', methods=["GET"])
def progress_bar():
    # while progr != 100:
    #     if progr != oldprogr:
    #         yield progr

    if progr is None:
        data = str(0) + "%"
    # if progr != oldprogr:
    #     return render_template('success.html', progr=progr)
    else:
         data = str(progr) + "%"

    return Response(data, mimetype='text/html', headers=None)

    


def success(task_id, deviceName):
    #voert progresschack uit zodat progr wordt veranderd
    #kijken om een async functie met thread?
    t1=threading.Thread(target=progress_check, args=(task_id,))
    thread_list.append(t1)
    t1.start()

    # t2=threading.Thread(target=progress_bar)
    # thread_list.append(t2)
    # t2.start()

    if progr is None:
        return render_template('success.html', targetname=deviceName)

    return render_template('success.html', targetname=deviceName)

#Report methods - reports.html
@app.route('/reports', methods=["GET"])
def reports_GET():
    return render_template('reports.html', tasks=task_list, reports=report_format_list)

@app.route('/reports', methods=["POST"])
def reports():
    return render_template('reports.html', tasks=task_list)

@app.route('/downloadreport', methods=["POST"])
def downloadreport():
    format = request.form.get("format")
    report_id = request.form.get("report_id")
    tasks.download_report(report_id, format)
    return reports_GET()

#Configure IP methods - config.html
@app.route('/configuration', methods=["GET"])
def config_GET():
    return render_template('config.html')

@app.route('/staticip', methods=["POST"])
def staticip():
    ip= request.form.get("ip")
    subnet=request.form.get("subnet")
    set_static_ip(ip, subnet)
    return render_template('config.html')

@app.route('/dhcp', methods=["POST"])
def dhcp():
    set_dhcp()
    return render_template('config.html')

@app.route('/portQuestions', methods=["POST"])
def portQuestions():
    with open("ports.txt", "r") as f:
            port_list = f.read()            
            port_list=re.findall(r'[\d]*[^,\sTU:]', port_list)
            print(port_list)
    targetname=request.form.get("targetname")
    print(targetname)
    return render_template('questions.html', ports=port_list, targetname=targetname)

@app.route('/portAnswers', methods=["POST"])
def portAnswers():
    AnswerList=dict()
    targetname=request.form.get("targetname")
    print(targetname)
    with open("ports.txt", "r") as f:
            port_list = f.read()           
            port_list=re.findall(r'[\d]*[^,\sTU:]', port_list)
    for port in port_list:
        yesno=request.form.get("inlineRadioOptions"+port)
        explanation=""
        explanation=request.form.get("textArea"+port)
        AnswerList[port]=[yesno, explanation]
    print(AnswerList)
    try:
        os.system("mkdir txtfiles")
    except:
        print("directory exists")

    os.system("touch txtfiles/answers_target_" + targetname)

    with open("txtfiles/answers_target_" + targetname, "w") as a:
        for port in port_list:
            a.write("port: " + port + " yes/no: " + AnswerList[port][0] + ", explanation: " + AnswerList[port][1] + "\n")
    zip_files(targetname)
    return index()
@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route('/scan')
def scann():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    app.run(debug=True)   
