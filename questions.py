import threading
import webbrowser
import os
import pwd

def questions():
    #thread_list=[]
    #print("questions thread started")
    #uid = pwd.getpwnam('kali')[2]
    #os.setuid(uid)
    #webbrowser.open('https://docs.google.com/forms/d/e/1FAIpQLSdBnpgfcMkY3wvy5mouEkjvFBbhbBXjrh-lw4o7nUeopZ-3Kw/viewform?usp=sf_link', new=1)
    os.system('sudo -usam xdg-open https://docs.google.com/forms/d/e/1FAIpQLSdBnpgfcMkY3wvy5mouEkjvFBbhbBXjrh-lw4o7nUeopZ-3Kw/viewform?usp=sf_link')
    #tquestions=threading.Thread(target=questions)
    #thread_list.append(tquestions)
    #tquestions.start()
