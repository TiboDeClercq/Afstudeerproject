import socket
from tkinter import *
from tkinter import messagebox

from scan import scan

ipList = []
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
    else:

        scan(deviceEntry.get(), ipList)

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
def succesPopUp(msg):
    succesPopUp = Tk()
    succesPopUp.wm_title("Succes message")
    succesPopUp.geometry("320x150")
    label = Label(succesPopUp, text="The scan has succesfully started.")
    label.pack(side="top", fill="x", pady=30)
    B1 = Button(succesPopUp, text="Okay", command = succesPopUp.destroy )
    B1.pack()
    succesPopUp.mainloop()

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

#Radiobuttons to choose deep scan or normal scan
Label (root, text="Type of scan",  fg="black", font="none 12").grid(row=5,column=0, sticky=W)
selected = IntVar()

rad1 = Radiobutton(root,text='Normal scan', value=1, variable=selected, width=20)
rad2 = Radiobutton(root,text='Hard scan', value=2, variable=selected, width=20)

rad1.grid(column=0, row=6)
rad2.grid(column=0, row=7)
    
#button to start the scan
Button(root, text="Scan", width=6, command=sendscan).grid(row=8, column=0, sticky=W)
Button(root, text="Pop", width=6, command=succesPopUp).grid(row=9, column=0, sticky=W)
root.mainloop()
