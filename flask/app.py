from flask import Flask, render_template, request, redirect, url_for
import socket, threading
import sys, os
from datetime import datetime
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scan import scan
from questions import questions
from setup import set_dhcp, set_static_ip
#from .. from setup import set_static_ip, set_dhcp
import re
app = Flask(__name__)

IpAddressen = []
errorList = []
report_list=[]


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
        scan(targetUniqueName, IpAddressen, conf_id)
        questions()
        IpAddressen[:]=[]
        return portQuestions()


#Report methods - reports.html
@app.route('/reports', methods=["GET"])
def reports_GET():
    return render_template('reports.html', reports=report_list)

@app.route('/reports', methods=["POST"])
def reports():
    return render_template('reports.html', reports=report_list)


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

@app.route('/portQuestions')
def portQuestions():
    with open("ports.txt", "r") as f:
            port_list = f.read()
            
            port_list=re.findall(r'[\d]*[^,\sTU:]', port_list)
            print(port_list)
    return render_template('questions.html', ports=port_list)
@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    app.run(debug=True)   
