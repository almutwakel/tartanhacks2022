from inspect import formatargvalues
from sys import displayhook
import tkinter
import threading
from tkinter import *

pcount = 0

root = Tk()
root.attributes("-fullscreen", False)

def make(): 
    alert = Toplevel()
    # alert.attributes("-toplevel", True)
    title = Label(alert, text = "p n u m b e r")
    text = Message(alert, text = pcount, font = 20000)
    title.pack()
    text.pack()
    return alert

# def display():
#     # title.pack()
#     text.configure(text = pcount, font = 20000)
#     # xButton.pack()
#     return

def pupdate():
    global pcount 
    pcount += 1
    print(pcount)


lookingAway = True
alert = None
while True:
    root.update()
    if lookingAway and alert is None : 
        # display()
        # alert.update()
        # root.deiconify() #may need this for toplevel
        # root.attributes('-topmost', True) #also not working for toplevel :()
        # root.after(5000, root.withdraw())

        pupdate()
        alert = make()


    elif not lookingAway and alert is not None :
        alert.destroy()