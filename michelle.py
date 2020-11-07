# homepage
import math, copy, random

from cmu_112_graphics import *


from cmu_112_graphics import *
import random
import string
import time

def appStarted(app):
    app.buttonWidth = 300
    app.buttonHeight = 200
    app.emailButton = False

def mousePressed(app, event):
    return None

def emailButton(app):
    return None

def drawButtons(app, canvas):
    for x in range(0, app.width, int(app.width/3)):
        for y in range(150, app.height - 100, int(app.height/2.5)):
            canvas.create_rectangle(x + 50, y, x + app.width/3 - 50, 
                                    y + app.buttonHeight, fill = 'blue')

def drawEmail(app, canvas):
    x, y = 50, 100

def redrawAll(app, canvas):
    drawButtons(app, canvas)

runApp(width=1250, height=750)