from flask import Flask, render_template, request
import socket, threading
#from .. import scan, questions
#from .. from setup import set_static_ip, set_dhcp



app = Flask(__name__)

IpAddressen = ["192.168.0.1"]

conf_id = "698f691e-7489-11df-9d8c-002264764cea"

@app.route("/addIP", methods=["POST"])
def addIP():
    entered_text=request.form.get("inputIP")
    IpAddressen.append(entered_text)
    if not entered_text:
        print("You haven't entered an IP address")
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route("/delIP", methods=["POST"])
def delIP():
    entered_text=request.form.get("delIP")
    IpAddressen.remove(entered_text)
    return render_template('index.html', IpAdressen=IpAddressen)

@app.route('/')
def index():
    return render_template('index.html', IpAdressen=IpAddressen)

if __name__ == "__main__":
    app.run(debug=True)        

#@app.route('/sendScan')
# def sendScan():
#     if not deviceEntry.get():
#         print("You haven't entered a device name.")
#     if not ipList:
#         print("You haven't entered any IP address.")
#     else:
#         print("Success")
#         scan(deviceEntry.get(), ipList, config_id)
#         questions()
#         ipList[:]=[]


#function to check if entered IP address is valid
# def valid_ip(address):
#     try: 
#         socket.inet_aton(address)
#         #if the entered IP address is not in the list -> add to list
#         if address in ipList:
#             print("This IP address is already in the list.")
#         else:
#             ipList.append(address)
#             return True
#     except:
#         print("This IP address is not valid.")
#         return False

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