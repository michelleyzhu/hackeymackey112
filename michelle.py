# homepage
import module_manager
module_manager.review()

import math, copy, random
from tkinter import *
from tkmacosx import Button
import random
import string
import time
import processTopics
import scraping_reps as sr
from dataclasses import make_dataclass
from quizClass import *
import makeEmail
import scrapeVoteRecords

def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("Election Dashboard")
root.configure(background = 'black')
root.geometry('1206x750')

main = Frame(root)
quiz = Frame(root)
ops = Frame(root)
results = Frame(root)
mail = Frame(root)
cand = Frame(root)
f5 = Frame(root)
victory = Frame(root)
f7 = Frame(root)
userInput = dict()

for frame in (main, quiz, mail, cand, ops, results, f5, victory, f7):
    frame.grid(row=0, column=0, sticky='news')

'''
Drawing banners
'''
# top banner
photo1 = PhotoImage(file = "pictures/flower.gif")
Label (main, image = photo1, bg = 'black') .grid(row=0, column=0, columnspan=3)
Label (main, text = 'Election Dashboard', bg = '#e8e3d3', fg = 'black', \
font = 'Times 60 bold') .grid(row=0, column=0, columnspan=3)

# bottom banner
photo2 = PhotoImage(file = "pictures/flowerbot.gif")
Label (main, image = photo2, bg = 'black') .grid(row = 3, column = 0, columnspan=3)

'''
Making buttons
'''
# buttons
w = 350 
h = 350
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
# search button
search = PhotoImage(file = "pictures/search.png")
Button (main, compound=TOP, text = 'candidate research', bg = bgcolor, 
fg = 'black', font = 'times 30 bold', width = w, height = h, image = search, \
command=lambda:raise_frame(cand)).grid(row = 1, column = 2)




'''
Generate email
'''
def generateEmail(politician, position):
    lastname = politician.split(' ')[-1]
    output.delete(0.0, END)
    pollink.insert(0.0, END)
    if position == 'representative':
        pos1 = 'House'
    else:
        pos1 = 'Senate'
    source1, content1, source2, content2 = makeEmail.generateQuoteAndSource(userInput['issue'])
    billnumber, billname, stance, url = scrapeVoteRecords.findIntroducedBills(userInput['topic'], pos1, userInput['issue'], userInput['party'])[0]
    view = None
    view1 = None
    if stance: 
        view = 'support'
        view1 = 'pass'
    else: 
        view = 'oppose'
        view1 = 'reject'
    emailText = f'''Dear {position} {politician}:
    My name is {userInput['name']} and I am a resident of {userInput['state']}. I am writing to you because 
    I am passionate about {userInput['issue']}, specifically requesting that you {view} {billnumber} {billname}.
    
    I believe that it is important for you to {view1} this measure for the following reasons:
    - According to {source1}, {content1}.
    - {content2}, as reported by {source2}.
    On a more personal note, [insert why you care about this issue].
    
    I know that you must be very busy, and I sincerely thank you for taking the time to read this. 
    I know that if you {view1} this bill, you will be improving the lives of many Americans, just like me.
    
    Best Regards, 
        {userInput['name']}
        '''
    output.insert(END, emailText)
    if position == 'representative':
        pollink.insert(f'https://{lastname}.house.gov/contact')
    else:
        pollink.insert(f"https://{lastname}.senate.gov/contact")

'''
Submit button
'''
def click():
    labeltext = ''
    politiciantext = ''
    gotZipcode = False
    gotState = False
    userInput['name'] = name.get()
    userInput['party'] = party.get()
    userInput['zipcode'] = zipcode.get()
    userInput['state'] = state.get()
    userInput['topic'] = topic1.get()
    userInput['issue'] = str(issue.get())
    if userInput['zipcode'] != None:
        try:
            houserep = sr.findHouseRep(userInput['zipcode'])
            politiciantext += 'Your house representative is: ' + houserep + '\n'
            gotZipcode = True
        except:
            labeltext += 'invalid zipcode    '
    if userInput['state'] != None and sr.findSenators(userInput['state']) != set():
        senators = sr.findSenators(userInput['state'])
        politiciantext += ' Your senators are: ' + ', '.join(senators)
        gotState = True
    else:
        labeltext += 'invalid state    '
    if gotZipcode and gotState and name.get() != None and party.get() != None and issue.get() != None:
        Label(mail, text = 'Information received, gathering data...', bg = 'white')\
        .grid(row = 10, column = 3, columnspan = 3, sticky = W)
    else:
        Label(mail, text = labeltext, bg = 'white') \
        .grid(row = 10, column = 3, columnspan = 3, sticky = W)
    if gotZipcode and gotState and name.get() != None and party.get() != None and issue.get() != None:
        Label(mail, text = politiciantext, bg = 'white') \
        .grid(row = 14, column = 2, columnspan = 3, sticky = W)
        senators = list(senators)
        Label(mail, text = 'Choose a politician to email: ', bg = 'pink', font = 'Arial 13 bold') \
        .grid(row = 13, column = 2, sticky = W)
        Button (mail, text = houserep, width = 100, command= lambda x=houserep: generateEmail(x, 'Representative') ) \
        .grid(row = 13, column = 3, columnspan = 3, sticky = W)
        Button (mail, text = senators[0], width = 100, command=lambda x=senators[0]: generateEmail(x, 'Senator')) \
        .grid(row = 13, column = 3, columnspan = 3)
        Button (mail, text = senators[1], width = 100, command=lambda x=senators[1]: generateEmail(x, 'Senator')) \
        .grid(row = 13, column = 3, columnspan = 3, sticky = E)


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

Label(mail, text='Party Affiliation (D or R): ',
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

Label(mail, text='Topic: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 8, column = 2, sticky = W)
topic1 = Entry(mail, width = 20, bg = 'white')
topic1.grid(row = 8, column = 3, sticky = W)

Label(mail, text='Specific Issue/Concern: ',
bg = 'pink', font = 'Arial 13 bold') .grid(row = 9, column = 2, sticky = W)
issue = Entry(mail, width = 20, bg = 'white')
issue.grid(row = 9, column = 3, sticky = W)

Label(mail, font = 'Arial 13 bold') .grid(row = 11, column = 2, rowspan = 1)
Button (mail, text = 'SUBMIT', width = 100, command=click) \
.grid(row = 11, column = 2, sticky = W)

Label(mail, font = 'Arial 13 bold') .grid(row = 12, column = 2)
output = Text (mail, width = 75, height = 20, wrap = WORD, bg = 'white') 
output.grid(row = 16, column = 2, columnspan = 3, sticky = W)

pollink = Text (mail, width = 75, height = 20, wrap = WORD, bg = 'white') 
pollink.grid(row = 17, column = 2, columnspan = 3, sticky = W)


# interest is yes, no or "unanswered"
topic = make_dataclass('topic', 
    ['name','interest', 'options', 'opinion','opinionSaved'])


'''
Make quiz
'''
# List of topics and their options
topicDict = {
    'legalized abortion' : ['pro-choice','pro-life'],
    'gun control' : ['favor gun control', 'oppose gun control'],
    'tax the ultra-wealthy' : ['favor wealth tax','oppose wealth tax'],
    'undocumented immigration' : ['favor immigration','support deportation']
}

# Initializing user responses to topics
responses = dict()
for t in topicDict:
    newTopic = topic(interest = "unanswered", name = t, 
        options=topicDict[t], opinionSaved = False, opinion = None)
    responses[t] = newTopic

generateInterestQuiz(frame,main,mail,quiz,ops,results,topicDict,responses,issue)
######################################################################
# ops page
######################################################################


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
