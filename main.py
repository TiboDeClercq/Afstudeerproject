from tkinter import *
import socket

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from gvm.protocols.gmpv9 import CredentialType
from gvm.protocols.gmpv9 import ScannerType
from gvm.protocols.gmpv9 import FilterType
import re
from xml.etree import ElementTree

#TODO
#deze code een beetje opkuisen

ipList = []
def addIP():
    entered_text=textentry.get()

    # if valid_ip(entered_text):
    #     print(entered_text)
    return valid_ip(entered_text)
#geen gebruik van regex voor het controleren van ip addres
def valid_ip(address):
    try: 
        socket.inet_aton(address)
        if address in ipList:
            print('Ip already in list')
        else:
            ipList.append(address)
            output.insert(END, address)
            return True
    except:
        return False

def scan():
    # if len(ipList) = 0:
    #     print('Geen ip addressen')
    # else:
    connection = UnixSocketConnection()
    transform = EtreeTransform()

    user_input=False

    def get_id(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'id=\"[0-9,a-z,-]*',xmlstr.decode('utf8'))
        return regexid[0][4:]

    def get_name(inputxml):
        xmlstr=ElementTree.tostring(inputxml, encoding='utf8', method='xml')
        regexid=re.findall(r'<name>[a-z]*</name>',xmlstr.decode('utf8'))
        return regexid

    with Gmp(connection, transform=transform) as gmp:
        # Login -> change to default admin password
        gmp.authenticate('tibo', 'tibo')
        
        if any("<name>scanner</name>" in s for s in get_name(gmp.get_users())):
            print("no new user created")
        else:
            #user creation
            user=gmp.create_user('scanner', password='scanner', role_ids=['7a8cb5b4-b74d-11e2-8187-406186ea4fc5'])
            user_id = get_id(user)
            print(user_id)


        #target creation
        #waarde uit de box halen
        target_name = deviceEntry.get()
        #entered_text=textentry.get()
        target=gmp.create_target(target_name, hosts=ipList)
        target_id = get_id(target)

        #task creation
        task=gmp.create_task(target_name, 'daba56c8-73ec-11df-a475-002264764cea', target_id, '08b69003-5fc2-4037-a479-93b440211c73')
        task_id = get_id(task)
        
        #task start
        gmp.start_task(task_id)
        print("task started succesfully!")


#layout
window = Tk()
window.title('Hallo')

Label (window, text="Ip address", bg="black", fg="white", font="none 12 bold").grid(row=0,column=0, sticky=W)
textentry = Entry(window, width= 20, bg="white")
textentry.grid(row=1,column=0,sticky=W)

output = Listbox(window, width=20, height=6,  background="white")
output.grid(row=0, column=4, sticky=W, rowspan=3)

# Label (window, text="Task name", bg="black", fg="white", font="none 12 bold").grid(row=5,column=0, sticky=W)
# textentry = Entry(window, width= 20, bg="white")
# textentry.grid(row=6,column=0,sticky=W)

Button(window, text="Add addres", width=6, command=addIP).grid(row=2, column=0, sticky=W)

Label (window, text="Device name", bg="black", fg="white", font="none 12 bold").grid(row=3,column=0, sticky=W)
deviceEntry = Entry(window, width= 20, bg="white")
deviceEntry.grid(row=4,column=0,sticky=W)

Button(window, text="Scan", width=6, command=scan).grid(row=8, column=0, sticky=W)
window.mainloop()