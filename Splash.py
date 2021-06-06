import tkinter as tk
import time
import os

import HB_Utilities


class Splash(tk.Toplevel):
    def __init__(self, parent, imagePath, delaySecond=3):
        tk.Toplevel.__init__(self, parent)

        print(os.getcwd())

        theImage = tk.PhotoImage(master=self, file=imagePath)
        w = theImage.width()
        h = theImage.height()

        # Trick to resize the image looking like 90% of the screen width
        theImage = theImage.zoom(10)
        scale_w = int(round(10/ (self.winfo_screenwidth() / w / (100/85))))
        scale_h = int(round(10/ (self.winfo_screenheight() / h / (100/85))))
        scale = max(scale_w, scale_h)
        theImage = theImage.subsample(scale)

        # get the resized size to center the window
        w = theImage.width()
        h = theImage.height()

        canvas1 = tk.Canvas(self, width=w, height=h, bg='white')
        item = canvas1.create_image(w/2, h/2, anchor=tk.CENTER, image=theImage)
        # Rajouter cette ligne
        canvas1.image = theImage
        canvas1.pack()

        HB_Utilities.RemoveTKBorders(self)

        windowWidth = w
        windowHeight = h
        print("Width", windowWidth, "Height", windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        geometryString = "+{}+{}".format(positionRight, positionDown)
        self.geometry(geometryString)

        ## required to make window show before the program gets to the mainloop
        self.update()

        ## simulate a delay while loading
        time.sleep(delaySecond)

        ## finished loading so destroy splash
        self.destroy()

        ## show window again
        if parent is not None:
            parent.deiconify()
