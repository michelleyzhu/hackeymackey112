import math, copy, random
from tkinter import *
from tkmacosx import Button
import random
import string
import time
import processTopics
import scraping_reps as sr
from dataclasses import make_dataclass


flexButts = {}

def raise_frame(frame):
    frame.tkraise()

def enterInterest(responses,topicDict,ops,level,t,oRow):
    undoHigh = (responses[t].interest == 'high')
    responses[t].interest = level
    if(responses[t].interest == 'high' and not undoHigh):
        flexButts[(t,"lab")] = Label (ops, text=t)
        flexButts[(t,'fir')] = Button (ops, text=topicDict[responses[t].name][0],\
            command=lambda x=t: enterOpinion(responses,topicDict[responses[t].name][0], x))
        flexButts[(t,'sec')] = Button (ops, text=topicDict[responses[t].name][1], \
            command=lambda x=t: enterOpinion(responses,topicDict[responses[t].name][1], x))

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

def enterOpinion(responses,opinion,t):
    responses[t].opinion = opinion
    for response in responses:
        print(response,responses[response].opinion)
    print("----end opinions---")

def updateResults():
    raise_frame(results)


def generateInterestQuiz(frame,main,quiz,ops,topicDict,responses):
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
    '''
    # Results Header
    rRow = 1
    Label (quiz, text='Political Alignment Quiz').grid(row = qRow,column = 1, columnspan = 3)
    qRow += 1
    Label (quiz, text='Here are your results.').grid(row = qRow,column = 1, columnspan = 3)
    qRow += 1
    '''
    # Buttons for selecting interest levels in each topic
    # Adds opinions within enterInterest
    for t in topicDict:
        Label (quiz, text=t).grid(row = qRow, column = 1)
        Button (quiz, text="low",command=lambda x=t: enterInterest(responses,topicDict,ops,'low', x,oRow))\
            .grid(row = qRow, column = 2)
        Button (quiz, text="high", command=lambda x=t: enterInterest(responses,topicDict,ops,'high', x,oRow))\
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
        command=lambda:updateResults())
    flexButts["home"] = Button (ops, text='Go to home screen', \
        command=lambda:raise_frame(main))
    for index in ['back',"submit","home"]:
            flexButts[index].grid(row = oRow[0], column = 1, columnspan = 3)
            oRow[0] += 1
