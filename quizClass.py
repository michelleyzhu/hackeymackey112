import math, copy, random
from tkinter import *
from tkmacosx import Button
import random
import string
import time
import scraping_reps as sr
from dataclasses import make_dataclass


flexButts = {}
def raise_frame(frame):
    frame.tkraise()

def enterInterest(responses,topicDict,mail,ops,results,resultsButtons,level,t,oRow,rRow,issue):
    undoHigh = (responses[t].interest == 'high')
    responses[t].interest = level
    if(responses[t].interest == 'high' and not undoHigh):
        flexButts[(t,"lab")] = Label (ops, text=t)
        flexButts[(t,'fir')] = Button (ops, text=topicDict[responses[t].name][0],\
            command=lambda x=t: enterOpinion(responses,topicDict,mail,results,resultsButtons,topicDict[responses[t].name][0], x,rRow,issue))
        flexButts[(t,'sec')] = Button (ops, text=topicDict[responses[t].name][1], \
            command=lambda x=t: enterOpinion(responses,topicDict,mail,results,resultsButtons,topicDict[responses[t].name][1], x,rRowissue))

        col = 1
        for index in ["lab","fir","sec"]:
            flexButts[(t,index)].grid(row = oRow[0], column = col)
            col += 1
        
        oRow[0] += 1
        for index in ['back',"submit","home"]:
            flexButts[index].grid(row = oRow[0], column = 1, columnspan = 3)
            oRow[0] += 1
    elif(undoHigh):
        print("trying to forget")
        for index in ["lab","fir","sec"]:
            flexButts[(t,index)].grid_forget()
            oRow[0] -= 1
        for index in ['back',"submit","home"]:
            flexButts[index].grid(row = oRow[0], column = 1, columnspan = 3)
            oRow[0] += 1

    for response in responses:
        print(response,responses[response].interest)
    print("----end levels---")



def enterOpinion(responses,topicDict,mail,results,resultsButtons,opinion,t,rRow,issue):
    sameOpinion = (responses[t].opinion == opinion)
    responses[t].opinion = opinion

    rRow += 1
    col = 1
    Label (results, text=f'select which issue to email about: ')\
        .grid(row = rRow,column = col)
    
    col += 1
    # Shows the buttons which have associated opinions
    for topicName in resultsButtons:
        if(responses[topicName].opinion != None):
            if(not sameOpinion):
                resultsButtons[responses[topicName].name] = Button (results, text=responses[topicName].opinion,\
                    command=lambda x=responses[topicName].opinion: goToMail(mail,x,issue))
                #resultsButtons[topicName] = Button (results, text=topicName + "m",\
                    #command=goToMail(mail,responses[topicName].opinion))
            resultsButtons[topicName].grid(row = rRow, column = col)
            col += 1

    numOpinions = 0
    currLeftists = 0
    for response in responses:
        if(responses[response].opinion != None):
            numOpinions += 1
            if(responses[response].opinion == topicDict[responses[response].name][0] ):# Then left
                currLeftists += 1
    
    rRow -= 1
    alignment = currLeftists/numOpinions
    alignStr = "right/Republican"
    if(alignment > 2/3):
        alignStr = "left/Democrat"
    elif(alignment > 1/3):
        alignStr = "center/moderate"
    Label (results, text=f'Here is your political alignment: {alignStr}')\
        .grid(row = rRow,column = 1, columnspan = 3)
    
    
    for response in responses:
        print(response,responses[response].opinion)
    print("----end opinions---")


def goToMail(mail,searchQuery,issue):
    #issue.grid_forget()
    #issue = Entry(mail, width = 20, bg = 'white')
    #issue.grid(row = 8, column = 3, sticky = W)
    print(searchQuery)
    raise_frame(mail)
    # passes in searchQuery somehow


def generateInterestQuiz(frame,main,mail,quiz,ops,results,topicDict,responses,issue):
    # Quiz Header
    qRow = 1
    Label (quiz, text='Political Alignment Quiz').grid(row = qRow,column = 1, columnspan = 3)
    qRow += 1
    Label (quiz, text='Please rate your interest \
        level in the following issues').grid(row = qRow,column = 1, columnspan = 3)
    qRow += 1
    
    # Opinions Header
    oRow = [1]
    Label (ops, text='Political Alignment Quiz').grid(row = oRow[0],column = 1, columnspan = 3)
    oRow[0] += 1
    Label (ops, text='Please choose the option which best \
        represents your opinions').grid(row = oRow[0],column = 1, columnspan = 3)
    oRow[0] += 1
    
    # Results Header
    rRow = 1
    Label (results, text='Political Alignment Quiz').grid(row = rRow,column = 1, columnspan = 3)
    rRow += 1
    resultsButtons = {}

    for response in responses:
        resultsButtons[responses[response].name] = Button (results, text=responses[response].opinion,\
            command=lambda x=responses[response].opinion: goToMail(mail,x,issue))
    
            

    # Buttons for selecting interest levels in each topic
    # Adds opinions within enterInterest
    for t in topicDict:
        Label (quiz, text=t).grid(row = qRow, column = 1)
        Button (quiz, text="low",command=lambda x=t: enterInterest(responses,topicDict,mail,ops,results,resultsButtons,'low', x,oRow,rRow,issue))\
            .grid(row = qRow, column = 2)
        Button (quiz, text="high", command=lambda x=t: enterInterest(responses,topicDict,mail,ops,results,resultsButtons,'high', x,oRow,rRow,issue))\
            .grid(row = qRow, column = 3)
        qRow += 1
    

    #Quiz footer
    Button (quiz, text='Submit interest levels(next)', \
        command=lambda:raise_frame(ops)).grid(row = qRow, column = 1, columnspan = 3)
    qRow += 1
    Button (quiz, text='Go to home screen', \
        command=lambda:raise_frame(main)).grid(row = qRow, column = 1, columnspan = 3)

    #Opinion footer
    flexButts["back"] = Button (ops, text='Return to quiz screen', \
        command=lambda:raise_frame(quiz))
    flexButts["submit"] = Button (ops, text='Submit opinions(next)', \
        command=lambda:raise_frame(results))
    flexButts["home"] = Button (ops, text='Go to home screen', \
        command=lambda:raise_frame(main))
    for index in ['back',"submit","home"]:
            flexButts[index].grid(row = oRow[0], column = 1, columnspan = 3)
            oRow[0] += 1
    
    #Results footer
    rRow += 3
    Button (results, text='Go to home screen', \
        command=lambda:raise_frame(main)).grid(row = rRow, column = 1, columnspan = 3)