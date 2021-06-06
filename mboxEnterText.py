from tkinter import *
import sys

import HB_Utilities


class mboxEnterTextPopupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        # top = self.top = master
        self.l = Label(top, text="Please enter the text")
        self.l.pack(padx=10, pady=10)
        self.e = Entry(top, width=30)
        self.e.pack(padx=10, pady=10)
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack(padx=10, pady=10)
        top.grab_set()  # make it modal
        HB_Utilities.CenterTK(top)
        self.e.focus()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()

# for test only

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.b = Button(master, text="click me!", command=self.popup)
        self.b.pack()
        self.b2 = Button(master, text="print value", command=lambda: sys.stdout.write(self.entryValue() + '\n'))
        self.b2.pack()

    def popup(self):
        self.w = mboxEnterTextPopupWindow(self.master)
        self.b["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"

    def entryValue(self):
        return self.w.value


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()
