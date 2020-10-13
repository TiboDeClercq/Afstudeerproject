import threading
import webbrowser
import os
import pwd
import os
#type of question t = text 
# y = yes or no


# def questions():
#     #thread_list=[]
#     #print("questions thread started")
#     #uid = pwd.getpwnam('kali')[2]
#     #os.setuid(uid)
#     #webbrowser.open('https://docs.google.com/forms/d/e/1FAIpQLSdBnpgfcMkY3wvy5mouEkjvFBbhbBXjrh-lw4o7nUeopZ-3Kw/viewform?usp=sf_link', new=1)
#     # os.system('sudo -ukali xdg-open https://docs.google.com/forms/d/e/1FAIpQLSdBnpgfcMkY3wvy5mouEkjvFBbhbBXjrh-lw4o7nUeopZ-3Kw/viewform?usp=sf_link')
#     #tquestions=threading.Thread(target=questions)
#     #thread_list.append(tquestions)
#     #tquestions.start()
#     retu

def getQuestions():
  with open("./questions.txt", "r") as i:
    content=i.readlines()

  questions=[x.strip() for x in content]
  return questions

def submitAnswers(answers):
  os.system("touch answers.txt")
  with open("answers.txt", "w") as p:
    questions=getQuestions()
    for i in range(len(questions)):
      p.write(questions[i])
      p.write(": ")
      p.write(answers[i])
      p.write("\n")
      p.write("##########")
      p.write("\n")
