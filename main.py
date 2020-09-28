import socket
from tkinter import *
from tkinter import messagebox

from scan import scan
from questions import questions
from setup import set_static_ip, set_dhcp

ipList = []
#Full and Fast Ultimate is default configuration
config_id = "698f691e-7489-11df-9d8c-002264764cea" 
def addIP():
    entered_text=textentry.get()
    if not entered_text:
        warningPopUp("You haven't entered an IP addres")
    return valid_ip(entered_text)
    

#function to check if entered IP address is valid
def valid_ip(address):
    try: 
        socket.inet_aton(address)

        #if the entered IP address is not in the list -> add to list
        if address in ipList:
            warningPopUp("This IP address is already in the list.")
        else:
            ipList.append(address)
            output.insert(END, address)
            return True
    except:
        warningPopUp("This IP address is not valid.")
        return False

#function to start the scan
def sendscan():
    if not deviceEntry.get():
        warningPopUp("You haven't entered a device name.")
    if not ipList:
        warningPopUp("You haven't entered any IP address.")
    else:
        succesPopUp
        scan(deviceEntry.get(), ipList, config_id)
        questions()
        ipList[:]=[]
        textentry.delete(0,'end')
        output.delete(0,'end')
        deviceEntry.delete(0,'end')
        

def sendIP():
    set_static_ip(ipEntry.get(), netmaskEntry.get())

#function to show warning message
def warningPopUp(msg):
    warningPopUp = Tk()
    warningPopUp.wm_title("Warning !")
    warningPopUp.geometry("320x150")
    label = Label(warningPopUp, text="Warning: " + msg)
    label.pack(side="top", fill="x", pady=30)
    B1 = Button(warningPopUp, text="Close", command = warningPopUp.destroy )
    B1.pack()
    warningPopUp.mainloop()

#function to show waiting message
def succesPopUp():
    succesPopUp = Tk()
    succesPopUp.wm_title("Succes message")
    succesPopUp.geometry("320x150")
    label = Label(succesPopUp, text="The scan has succesfully started.")
    label.pack(side="top", fill="x", pady=30)
    B1 = Button(succesPopUp, text="Okay", command = succesPopUp.destroy )
    B1.pack()
    succesPopUp.mainloop()
#Full and  fast              daba56c8-73ec-11df-a475-002264764cea
#Full and Fast Ultimate      698f691e-7489-11df-9d8c-002264764cea
#Full and very Deep          708f25c4-7489-11df-8094-002264764cea
#Full and very Deep Ultimate 74db13d6-7489-11df-91b9-002264764cea
def change_config_id(*args):
    selectedType = tkvar.get() 
    
    type
    if selectedType == 'Full and Fast':
        config_id = "daba56c8-73ec-11df-a475-002264764cea"
        print(config_id)
    elif selectedType == 'Full and Fast Ultimate':
        config_id = "698f691e-7489-11df-9d8c-002264764cea"
        print(config_id)
    elif selectedType == 'Full and very Deep':
        config_id = "708f25c4-7489-11df-8094-002264764cea"
        print(config_id)
    elif selectedType == 'Full and very Deep Ultimate':
        config_id = "74db13d6-7489-11df-91b9-002264764cea"
        print(config_id) 
    else:
        print("niks")

#layout
root = Tk()
root.title('OpenVAS automated scanner')

#label and input for IP address
Label (root, text="Ip address", fg="black", font="12").grid(row=0,column=0, sticky=W)
textentry = Entry(root, width= 20, bg="white")
textentry.grid(row=1,column=0,sticky=W)

#list of IP addresses
output = Listbox(root, width=20, height=6,  background="white")
output.grid(row=0, column=4, sticky=W, rowspan=6)

#button to add IP address to list
Button(root, text="Add address", width=7, command=addIP).grid(row=2, column=0, sticky=W)

#label and input for target name
Label (root, text="Device name", fg="black", font="12").grid(row=3,column=0, sticky=W)
deviceEntry = Entry(root, width= 20, bg="white")
deviceEntry.grid(row=4,column=0,sticky=W)

#Radiobuttons to choose deep scan or Full and Fast Ultimate
Label (root, text="Type of scan",  fg="black", font="none 12").grid(row=5,column=0, sticky=W)
tkvar = StringVar(root)
# Dictionary with options
choices = { 'Full and Fast','Full and Fast Ultimate','Full and very Deep','Full and very Deep Ultimate'}
tkvar.set('Full and Fast Ultimate') # set the default option

popupMenu = OptionMenu(root, tkvar, *choices)
popupMenu.grid(row = 6, column =0)
# link function to change dropdown
tkvar.trace('w', change_config_id)
#button to start the scan
Button(root, text="Scan", width=6, command=sendscan).grid(row=8, column=0, sticky=W)

Label (root, text="ip address", fg="black", font="none 12").grid(row=10,column=0, sticky=W)
ipEntry=Entry(root, width= 20, bg="white")
ipEntry.grid(row=10, column=5, sticky=W)

Label (root, text="netmask", fg="black", font="none 12").grid(row=11,column=0, sticky=W)
netmaskEntry=Entry(root, width= 20, bg="white")
netmaskEntry.grid(row=11, column=5, sticky=W)

Button(root, text="set static ip address", width=10, command=sendIP).grid(row=12, column=0, sticky=W)
Button(root, text="set dhcp", width=6, command=set_dhcp).grid(row=14, column=0, sticky=W)

root.mainloop()