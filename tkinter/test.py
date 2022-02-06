import time
from inspect import formatargvalues
from sys import displayhook
import tkinter
import random
from tkinter import *

pcount = 0

root = Tk()
root.attributes("-fullscreen", False)
# k and l are gone
letters = ["ᔑ", "ʖ", "ᓵ", "↸", "ᒷ", "⎓", "⊣", "⍑", "╎", "⋮", "ᒲ", "リ", "𝙹", 
"!", "¡", "ᑑ", "∷", "ᓭ", "ℸ ̣", "⚍", "⍊", "∴", " ̇/", "||", "⨅"]


def make():
    alert = Toplevel()
    alert.configure(bg='#ede0ce')
    # alert.attributes("-toplevel", True)
    title = Label(alert, bg = '#ede0ce', text = "p n u m b e r")
    if(random.random() < 0.5):
        text = Message(alert, bg = '#ede0ce',text = pcount, font = ("Arial", 200))
    else:
        text = Message(alert, bg = '#ede0ce',text = random.choice(letters), font = ("Arial", 200))

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
        #lookingAway = False
        time.sleep(5)

    elif not lookingAway and alert is not None:
        alert.destroy()
        alert = None
        lookingAway = True
