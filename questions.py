import threading
import webbrowser
import os
import pwd
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
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
