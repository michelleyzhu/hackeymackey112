# homepage
import math, copy, random
from tkinter import *
from tkmacosx import Button
import random
import string
import time
import processTopics
import scraping_reps as sr
from dataclasses import make_dataclass
from quizClass import generateInterestQuiz

def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("Election Dashboard")
root.configure(background = 'black')
root.geometry('1206x750')

main = Frame(root)
quiz = Frame(root)
ops = Frame(root)
mail = Frame(root)
cand = Frame(root)
f5 = Frame(root)
victory = Frame(root)
f7 = Frame(root)
userInput = dict()

for frame in (main, quiz, mail, cand, ops, f5, victory, f7):
    frame.grid(row=0, column=0, sticky='news')

'''
Drawing banners
'''
# top banner
photo1 = PhotoImage(file = "pictures/flowers.gif")
Label (main, image = photo1, bg = 'black') .grid(row=0, column=0, columnspan=3)
Label (main, text = 'Election Dashboard', bg = '#e8e3d3', fg = 'black', \
font = 'Times 50 bold') .grid(row=0, column=0, columnspan=3)

# bottom banner
photo2 = PhotoImage(file = "pictures/flowerbot.gif")
Label (main, image = photo2, bg = 'black') .grid(row = 3, column = 0, columnspan=3)

'''
Making buttons
'''
# buttons
w = 350 
h = 250
bgcolor = '#fff4cf'
main.configure(background = '#e8e3d3')
# quiz button
quizimage = PhotoImage(file = "pictures/question-mark.png")
Button (main, compound=TOP, text = 'political alignment quiz', font = 'times 30 bold', 
width = w, height = h, bg = bgcolor, fg = 'black', image = quizimage, 
command=lambda:raise_frame(quiz)) .grid(row = 1, column = 0)
# mail button
mailimage = PhotoImage(file = "pictures/important-mail.png")
Button (main, compound=TOP, text = 'send mail', image = mailimage, bg = bgcolor, 
fg = 'black', font = 'times 30 bold', width = w, height = h, \
command=lambda:raise_frame(mail)).grid(row = 1, column = 1)
# random button
search = PhotoImage(file = "pictures/search.png")
Button (main, compound=TOP, text = 'candidate research', bg = bgcolor, 
fg = 'black', font = 'times 30 bold', width = w, height = h, image = search, \
command=lambda:raise_frame(cand)).grid(row = 1, column = 2)
# random button
Button (main, compound=TOP, text = 'idk', bg = bgcolor, 
fg = 'black', font = 'times 30 bold', width = w, height = h,  \
command=lambda:raise_frame(f5)).grid(row = 2, column = 0)
# random button
victory = PhotoImage(file = "pictures/victory.png")
Button (main, compound=TOP, text = 'path to victory', bg = bgcolor, image = victory,
fg = 'black', font = 'times 30 bold', width = w, height = h, \
command=lambda:raise_frame(victory)).grid(row = 2, column = 1)
# random button
Button (main, compound=TOP, text = 'idk', bg = bgcolor, 
fg = 'black', font = 'times 20 bold', width = w, height = h, \
command=lambda:raise_frame(f7)).grid(row = 2, column = 2)




# interest is yes, no or "unanswered"
topic = make_dataclass('topic', 
    ['name','interest', 'options', 'opinion','opinionSaved'])


'''
Make quiz
'''
# List of topics and their options
topicDict = {
    'legalized abortion' : ['pro-life', 'pro-choice'],
    'gun rights' : ['favor gun control', 'oppose gun control'],
    'tax the ultra-wealthy' : ['oppose wealth tax', 'favor wealth tax'],
    'undocumented immigration' : ['support deportation', 'favor assimilation']
}

# Initializing user responses to topics
responses = dict()
for t in topicDict:
    newTopic = topic(interest = "unanswered", name = t, 
        options=topicDict[t], opinionSaved = False, opinion = None)
    responses[t] = newTopic

generateInterestQuiz(main,quiz,ops,topicDict,responses)
######################################################################
# ops page
######################################################################



'''
Submit buttom
'''
def click():
    userInput['name'] = name.get()
    userInput['party'] = party.get()
    userInput['zipcode'] = zipcode.get()
    userInput['state'] = state.get()
    userInput['issue'] = issue.get()
    Label(mail, text = 'Information received, gathering data...', bg = 'white') \
    .grid(row = 10, column = 3, columnspan = 3, sticky = W)
    output.delete(0.0, END)
    if userInput['zipcode'] != None:
        try:
            output.insert(END, 'Your house representative is: ' + sr.findHouseRep(userInput['zipcode']))
        except:
            output.insert(END, 'invalid zipcode')
    if userInput['state'] != None and sr.findSenators(userInput['state']) != set():
        output.insert(END, '\nYour senators are: ' + ', '.join(sr.findSenators(userInput['state'])))
    else:
        output.insert(END, '\ninvalid state')
    

'''
Make mail
'''
Label(mail, text='Send Mail', font = 'Arial 30 bold') \
.grid(row = 1, column = 2, columnspan = 2)
Button(mail, text='Go to home screen', command=lambda:raise_frame(main)) \
.grid(row = 0, column = 0)
Label(mail, text='Please fill in the blanks. Use correct grammar and spelling.',
bg = 'light blue', font = 'Arial 13 bold') .grid(row = 2, column = 2, columnspan = 2)
Label(mail, font = 'Arial 13 bold') .grid(row = 3, column = 2)
Label(mail, text='Name: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 4, column = 2, sticky = W)
name = Entry(mail, width = 20, bg = 'white')
name.grid(row = 4, column = 3, sticky = W)
Label(mail, text='Party Affiliation: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 5, column = 2, sticky = W)
party = Entry(mail, width = 20, bg = 'white')
party.grid(row = 5, column = 3, sticky = W)
Label(mail, text='Zipcode: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 6, column = 2, sticky = W)
zipcode = Entry(mail, width = 20, bg = 'white')
zipcode.grid(row = 6, column = 3, sticky = W)
Label(mail, text='State (Not abbreviated): ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 7, column = 2, sticky = W)
state = Entry(mail, width = 20, bg = 'white')
state.grid(row = 7, column = 3, sticky = W)
Label(mail, text='Issue/Concern: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 8, column = 2, sticky = W)
issue = Entry(mail, width = 20, bg = 'white')
issue.grid(row = 8, column = 3, sticky = W)
Label(mail, font = 'Arial 13 bold') .grid(row = 9, column = 2, rowspan = 1)
Button (mail, text = 'SUBMIT', width = 100, command=click) \
.grid(row = 10, column = 2, sticky = W)
Label(mail, font = 'Arial 13 bold') .grid(row = 11, column = 2)
output = Text (mail, width = 75, height = 20, wrap = WORD, bg = 'white') 
output.grid(row = 13, column = 2, columnspan = 3, sticky = W)

'''
Make research
'''
Label(cand, text='Candidate Research').pack()
Button(cand, text='Go to home screen', command=lambda:raise_frame(main)).pack()

'''
Get representatives

senator, houserep = None, None
# dictionary of representatives
senator = sr.findSenators(userInput[zipcode])
# dictionary of representatives
houserep = sr.findHouseRep(userInput[state])
'''
# run
raise_frame(main)
root.mainloop()

    
'''
# start app
app = Tk()
app.title("Election Dashboard")
app.configure(background = 'white')

# top banner
photo1 = PhotoImage(file = "totoro.gif")
Label (app, image = photo1, bg = 'black') \
.grid(row = 0, column = 0, sticky = E)

Label (app, text = 'Dashboard', bg = 'black', fg = 'white', font = 'none 50 bold') \
.grid(row = 0, column = 0)

# make button
Button (app, text = 'mail', bg = 'pink', fg = 'black', font = 'none 12 bold', \
width = '40', height = '20', command = click .grid(row = 1, column = 0, sticky = W)

# text entry box
#textentry = Entry(app, width = 20, bg = 'white')
#textentry.grid(row = 2, column = 0, sticky = W)
'''
'''
def appStarted(app):
    app.buttonWidth = 300
    app.buttonHeight = 200
    app.email = False
    app.bXY = dict()
    buttonXY(app)

def mousePressed(app, event):
    if event.y >= app.bXY['email'][1] and event.y <= app.bXY['email'][3]:
        if event.x >= app.bXY['email'][0] and event.x <= app.bXY['email'][2]:
            app.email = True 

def buttonXY(app):
    buttons = ('none1', 'email', 'none2', 'none3', 'none4', 'none5')
    i = 0
    for y in range(150, app.height - 100, int(app.height/2.5)):
        for x in range(0, app.width - 20, int(app.width/3)):
            x1 = x + 50
            y1 = y
            x2 = x + app.width/3 - 50
            y2 = y + app.buttonHeight
            app.bXY[buttons[i]] = (x1, y1, x2, y2)
            i += 1

def drawButtons(app, canvas):
    for button in app.bXY:
        (x1, y1, x2, y2) = app.bXY[button]
        canvas.create_rectangle(x1, y1, x2, y2, fill = 'pink')

def drawEmail(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'white')

def redrawAll(app, canvas):
    drawButtons(app, canvas)
    if app.email:
        drawEmail(app, canvas)

runApp(width=1243, height=750)
'''
