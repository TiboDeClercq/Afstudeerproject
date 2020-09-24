import socket
from tkinter import *
from scan import scan
from tkMessageBox import showerror

ipList = []
def addIP():
    entered_text=textentry.get()
    return valid_ip(entered_text)

#function to check if entered IP address is valid
def valid_ip(address):
    try: 
        socket.inet_aton(address)

        #if the entered IP address is not in the list -> add to list
        if address in ipList:
            print('Ip already in list')
        else:
            ipList.append(address)
            output.insert(END, address)
            return True
    except:
        return False

#function to start the scan
def sendscan():
    if deviceEntry.get():
        Tk().withdraw()
        showerror(title = "Error", message = "Something bad happened")
    else:
        scan(deviceEntry.get(), ipList)
    

#layout
window = Tk()
window.title('OpenVAS automated scanner')

#label and input for IP address
Label (window, text="Ip address", bg="black", fg="white", font="none 12 bold").grid(row=0,column=0, sticky=W)
textentry = Entry(window, width= 20, bg="white")
textentry.grid(row=1,column=0,sticky=W)

#list of IP addresses
output = Listbox(window, width=20, height=6,  background="white")
output.grid(row=0, column=4, sticky=W, rowspan=3)

#button to add IP address to list
Button(window, text="Add address", width=7, command=addIP).grid(row=2, column=0, sticky=W)

#label and input for target name
Label (window, text="Device name", bg="black", fg="white", font="none 12 bold").grid(row=3,column=0, sticky=W)
deviceEntry = Entry(window, width= 20, bg="white")
deviceEntry.grid(row=4,column=0,sticky=W)



#Radiobuttons to choose deep scan or normal scan
Label (window, text="Type of scan",  fg="black", font="none 12").grid(row=5,column=0, sticky=W)
selected = IntVar()

rad1 = Radiobutton(window,text='Normal scan', value=1, variable=selected, width=20)
rad2 = Radiobutton(window,text='Hard scan', value=2, variable=selected, width=20)

rad1.grid(column=0, row=6)
rad2.grid(column=0, row=7)

#button to start the scan
Button(window, text="Scan", width=6, command=sendscan).grid(row=8, column=0, sticky=W)
window.mainloop()