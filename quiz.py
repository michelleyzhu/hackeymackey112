import math, copy, random
from tkinter import *
from tkmacosx import Button
import random
import string
import time
import processTopics
import scraping_reps as sr
from dataclasses import make_dataclass

def enterInterest(responses,level,t):
    responses[t].interest = level
    for response in responses:
        print(response,responses[response].interest)

def generateInterestQuiz(main,quiz,ops,topicDict,responses):
    # Quiz Header
    Label (quiz, text='Political Alignment Quiz').grid(row = 1,column = 1, columnspan = 3)
    Label (quiz, text='Please rate your interest \
        level in the following issues').grid(row = 2,column = 1, columnspan = 3)
    
    # Buttons for selecting interest levels in each topic
    rowCount = 3

    for t in topicDict:
        Label (quiz, text=t).grid(row = rowCount, column = 1)
        Button (quiz, text="low",command=lambda x=t: enterInterest(responses,'low', x))\
            .grid(row = rowCount, column = 2)
        Button (quiz, text="high", command=lambda x=t: enterInterest(responses,'high', x))\
            .grid(row = rowCount, column = 3)
        rowCount += 1

    #Quiz footer
    Button (quiz, text='Submit interest levels(next)', \
        command=lambda:raise_frame(ops)).grid(row = rowCount, column = 1, columnspan = 3)
    rowCount += 1
    Button (quiz, text='Go to home screen', \
        command=lambda:raise_frame(main)).grid(row = rowCount, column = 1, columnspan = 3)