from tkinter import *
import socket

#TODO
#field voor taskname en devicename
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