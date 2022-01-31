from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askyesno
import numpy as np
import cv2 as cv
from pynput.mouse import Listener
from PIL import ImageGrab, Image

tracker = np.zeros((2, 2), 'int16')
shot = False

def onMouseDown(*args):
    global tracker, shot
    if args[-1] and not shot:
        tracker[0] = args[:2]

    elif not args[-1] and np.all(tracker[0] != 0) and not shot:
        tracker[1] = args[:2]
        screenshot = np.asarray(ImageGrab.grab())
        if np.all(tracker[1] > tracker[0]):
            cropped_ = screenshot[tracker[0, 1]:tracker[1, 1], tracker[0, 0]:tracker[1, 0]]
        else:
            cropped_ = screenshot[tracker[1, 1]:tracker[0, 1], tracker[1, 0]:tracker[0, 0]]    
        cropped = cv.cvtColor(cropped_, cv.COLOR_BGR2RGB)
        cv.imshow('Screenshot', cropped)
        shot = True
        cv.waitKey(0)
        msgbox = askyesno('Save File', 'Save File?')
        if msgbox:
            files = [('All Files', '*.*'),
            ('Jpeg file', '*.jpg'),
            ('PNG file', '*.png')
            ]
            file = asksaveasfile(mode="wb", initialfile="screenshot.png", initialdir=r'C:\Users\ACER\Documents', filetypes=files, defaultextension='*.png')
            Image.fromarray(cropped).save(file)
        return False

if __name__ == "__main__":
    with Listener(on_click=onMouseDown) as listner:
        listner.join()
