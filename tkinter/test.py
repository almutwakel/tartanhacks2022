from inspect import formatargvalues
from sys import displayhook
import tkinter
import threading
from tkinter import *

pcount = 0

# def make(): 
root = Tk()
root.attributes("-fullscreen", False)

title = Label(root, text = "p n u m b e r")
text = Message(root, text = pcount, font = 20000)
# xButton = Button(root, text="x", command=root.destroy)

title.pack()
text.pack()
# xButton.pack()
# return root


def display():
    # title.pack()
    text.configure(text = pcount, font = 20000)
    # xButton.pack()

def pupdate():
    global pcount 
    pcount += 1
    print(pcount)


lookingAway = True
while(True):
    if(lookingAway): 
        display()
        root.update()
        # root.deiconify() #may need this for toplevel
        # root.attributes('-topmost', True) #also not working for toplevel :()
        root.after(5000, root.withdraw())

        pupdate()

        # display()
        #root.destroy()
        # root = make()

        # pupdate()
        # root.after(4000, root.destroy())

# b = True
# while(b):
#     print(1)
#     b = False
    # root.mainloop()
