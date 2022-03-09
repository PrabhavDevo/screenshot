from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askyesno
import numpy as np
import cv2 as cv
from pynput.mouse import Listener
from PIL import ImageGrab, Image

tracker = np.zeros((2, 2), 'uint16') #for keeping track of cursor position, 2 dimensional because one is of starting pos and other is ending pos

def onMouseDown(*args):
    global tracker #because this function executes always on mouse click, so to let 'em not reset
    if args[-1]: #args[-1] refers to whether it was starting or pause. True means mouse is being held and False, well, not being held
        tracker[0] = args[:2] #setting the starting pos

    elif not args[-1] and np.all(tracker[0] != 0): #if it's the ending pos
        tracker[1] = args[:2] #setting the pos
        screenshot = np.asarray(ImageGrab.grab()) #taking a screenshot
        if np.all(tracker[1] > tracker[0]): #setting the starting position accordingly
            cropped_ = screenshot[tracker[0, 1]:tracker[1, 1], tracker[0, 0]:tracker[1, 0]] #if starting pos > ending pos, then it's the starting pos
        else:
            cropped_ = screenshot[tracker[1, 1]:tracker[0, 1], tracker[1, 0]:tracker[0, 0]] #if not, then the ending pos    
            
        bg_to = cv.COLOR_RGBA2BGRA if platform.system() == "Darwin" else cv.COLOR_RGB2BGR #setting default color space of os, BGRA and RGBA is default in MacOS while BGR and RGB in Windows and GNU/Linux
        cropped = cv.cvtColor(cropped_, bg_to) #converting to RGB/RGBA to avoid color conflicts
        cv.imshow('Screenshot', cropped)
        cv.waitKey(0)
        msgbox = askyesno('Save File', 'Save File?')
        if msgbox:
            files = [('All Files', '*.*'),
            ('Jpeg file', '*.jpg'),
            ('PNG file', '*.png')
            ]
            file = asksaveasfile(mode="wb", initialfile="screenshot.png", filetypes=files, defaultextension='*.png') # get path of where file has to be saved
            Image.fromarray(cropped).save(file) #save it
        return False #return false to stop event listner

if __name__ == "__main__":
    with Listener(on_click=onMouseDown) as listner:
        listner.join() #start the listner
