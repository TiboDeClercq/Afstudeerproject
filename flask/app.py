from flask import Flask, render_template, request
import socket, threading
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scan import scan
from questions import questions
#from .. from setup import set_static_ip, set_dhcp
import re
app = Flask(__name__)

IpAddressen = []
errorList = []

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
    IpAddressen.remove(entered_text)
    return render_template('index.html', IpAdressen=IpAddressen)     

@app.route('/sendScan', methods=["POST"])
def sendScan():
    try:
        conf_id=request.form.get("conf")
        deviceName= request.form.get("inputName")
        if not deviceName:
            print("You haven't entered a device name.")
        if not IpAddressen:
            print("You haven't entered any IP address.")
        else:
            print("Success")
            scan(deviceName, IpAddressen, conf_id)
            questions()
            IpAddressen[:]=[]
            return render_template('success.html')
    except:
        errorList.append('kapooooot')
        print('Da werkt niet he')
@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    app.run(debug=True)   

# def printIPList():
#     threading.Timer(5.0, printIPList).start()
#     print("<ul>")
#     for s in IpAddressen:
#         ul = "<li>" + str(s) + "</li>"
#         print(ul)
#     print("</ul>")

#function to start the scan     

# @app.route('/printTesten')
# def printTesten():
#     for i in range(4):
#         print('samen eten we m&m')
#     return 'dit is mijn statement'