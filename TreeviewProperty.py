import tkinter
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename  # idem for load
from mbox import MessageBox


class TreeviewProperty(ttk.Treeview):

    def __init__(self, mainWindow, parent, book, *args, **kwargs):
        self.parent = parent
        self.mainWindow = mainWindow
        self.book = book
        self.lastSelectedID = None
        self.lastObjectType = None
        self.selectedID = None
        self.selectedObjectType = None
        self.selectedObject = None

        self.attributeList = None
        self.attributeValue = None

        columns = ("Attribute", "Value")
        ttk.Treeview.__init__(self, master=parent, height=18, show="headings", columns=columns)

        self.column("Attribute", width=20, anchor='center')  # indicates column, not displayed
        self.column("Value", width=200, anchor='w')

        self.heading("Attribute", text="Attribute")  # Show header
        self.heading("Value", text="Value")

        self.place(x=0, y=40)

        self.pack(side=BOTTOM, fill=BOTH)

        self.rowIDCounter = 0

        self.popupID = tkinter.Menu(self.parent, tearoff=0)
        self.popupID.add_command(label="Copy object ID", command=self.CopyID)
        self.popupID.add_separator()
        self.popupID.add_command(label="Close popup menu")

        self.bind("<Button-3>", self.askForPopup)

        def mbox(msg, b1, b2, parent, cbo=False, cboList=[]):
            msgbox = MessageBox(msg, b1, b2, parent, cbo, cboList)
            msgbox.root.mainloop()
            msgbox.root.destroy()
            return msgbox.returning

        def set_cell_value(event):  # Double click to enter the edit state

            def hideButtons():
                entryedit.destroy()
                cancelBtn.destroy()
                okBtn.destroy()
                fileBtn.destroy()
                pageBtn.destroy()

            def canceledit():
                hideButtons()

            def saveedit():
                newValue = entryedit.get(0.0, "end")
                # solve problem : final \n to remove
                newValue = newValue.replace('\n', '').replace('\r', '').strip()
                hideButtons()
                self.set(item, column=column, value=newValue)
                theChangedAttribute = self.attributeList[rn-1]
                self.SaveAttributeChange(theChangedAttribute, newValue)

            def ChoosePage():

                allowedItems = self.book.getAllpagesList()
                prompt = dict()
                prompt['answer'] = mbox('Select page', ('Take', 'take'), ('Cancel', 'cancel'), self.mainWindow,
                                        cbo=True, cboList=allowedItems)
                ans = prompt['answer'].strip()
                print(ans)
                theSelectedID = self.book.getPageIDFromDisplayedText(ans)

                if theSelectedID != '':
                    entryedit.delete('1.0', END)
                    entryedit.insert("end-1c", theSelectedID)

            def openFile():
                filename = askopenfilename(initialdir=".", filetypes=[("Asset files", "*.*")], title="Choose an asset file ...", parent=self.parent)
                if filename != "":
                    entryedit.insert("end-1c", filename)

            for item in self.selection():
                column = self.identify_column(event.x)  # column
                row = self.identify_row(event.y)  # row
            cn = int(str(column).replace('#', ''))
            rn = int(str(row).replace('I', ''))
            if cn == 2 and rn > 1:  # only edit the 2nd column with values, not attribute names. And don't edit ID
                elementBox = self.bbox(self.selection(), "Value")
                entryedit = Text(self.parent, width=100, height=1)
                entryedit.place(x=elementBox[0], y=elementBox[1])
                textVal = self.set(item, column="Value")
                entryedit.insert("end-1c", textVal)
                okBtn = ttk.Button(self.parent, text='OK', width=4, command=saveedit)
                okBtn.place(x=elementBox[0]-8*16, y=elementBox[1])
                cancelBtn = ttk.Button(self.parent, text=' X ', width=4, command=canceledit)
                cancelBtn.place(x=elementBox[0]-6*16, y=elementBox[1])
                fileBtn = ttk.Button(self.parent, text='File', width=4, command=openFile)
                fileBtn.place(x=elementBox[0]-4*16, y=elementBox[1])
                pageBtn = ttk.Button(self.parent, text='Page', width=4, command=ChoosePage)
                pageBtn.place(x=elementBox[0]-2*16, y=elementBox[1])
                entryedit.focus()

        self.bind('<Double-1>', set_cell_value)  # Double-click the left button to enter the edit

        for col in columns:  # bind function to make the header sortable
            self.heading(col, text=col)

        self.FillContent()
        return

    def askForPopup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.identify_row(event.y)
        if iid and str(iid) == '0001':
            # mouse pointer over item
            self.selection_set(iid)
            try:
                self.popupID.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self.popupID.grab_release()
        else:
            # mouse pointer not over ID item
            # no action required
            pass
        return

    def CopyID(self):
        # self.selectedID

        self.clipboard_clear()
        self.clipboard_append(self.selectedID)
        self.update()  # now it stays on the clipboard
        return

    def EmptyContent(self):
        self.delete(*self.get_children())
        self.rowIDCounter = 0
        return

    def FillContent(self):

        def next_id():
            self.rowIDCounter += 1
            return "%.4d" % self.rowIDCounter

        self.EmptyContent()
        if self.attributeList is not None and self.attributeValue is not None:
            # if attribute is ID add a right mouse menu ...
            for i in range(min(len(self.attributeList), len(self.attributeValue))):  # write data
                if i % 2 == 0:
                    self.insert('', i, id=next_id(), values=(self.attributeList[i], self.attributeValue[i]))
                else:
                    self.insert('', i, id=next_id(), values=(self.attributeList[i], self.attributeValue[i]), tag='gray')
        self.tag_configure('gray', background='#cccccc')
        return

    def SelectionChanged(self, newID, obj):
        # empty the treeview
        self.EmptyContent()
        # reset local members of last selection

        # if new selection valid store to local members
        newType = newID[0:2]
        self.selectedObjectType = newType
        self.selectedID = newID
        self.selectedObject = obj

        # fill list with attribute names and values
        if newType == "_P":
            self.FillGridWithPage()
        elif newType == "PC":
            self.FillGridWithPageChoice()
        elif newType == "_O":
            self.FillGridWithObject()
        elif newType == "_M":
            self.FillGridWithMonster()
        elif newType == "_E":
            self.FillGridWithEnigm()
        elif newType == "_H":
            self.FillGridWithPossibleHero()
        elif newType == "Bo":
            self.FillGridWithBook()
        # fill treeview
        self.FillContent()
        return

    def SaveAttributeChange(self, attribute, newValue):
        # fill list with attribute names and values
        if self.selectedObjectType == "_P":
            self.SavePageAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "PC":
            self.SavePageChoiceAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "_O":
            self.SaveObjectAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "_M":
            self.SaveMonsterAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "_E":
            self.SaveEnigmAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "_H":
            self.SavePossibleHeroAttributeChange(attribute, newValue)
        elif self.selectedObjectType == "Bo":
            self.SaveBookAttributeChange(attribute, newValue)
        return

    def getEnteredBoolean(self, val):
        if val == True or val == 'True':
            return True
        return False

    def getEnteredFloat(self, val):
        ret = 0.0
        try:
            ret = float(val)
        except:
            print('Exception when try to convert '+val+' to float ... returned 0.0')
            pass
        return ret

    def FillGridWithPage(self):

        aPage = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(aPage.ID)

        self.attributeList.append("author")
        self.attributeValue.append(aPage.author)

        self.attributeList.append("creationDate")
        self.attributeValue.append(aPage.creationDate)

        self.attributeList.append("title")
        self.attributeValue.append(aPage.title)

        self.attributeList.append("comment")
        self.attributeValue.append(aPage.comment)

        self.attributeList.append("isFirstPage")
        self.attributeValue.append(aPage.isFirstPage)

        self.attributeList.append("backgroundImage")
        self.attributeValue.append(aPage.backgroundImage)

        self.attributeList.append("backgroundMusic")
        self.attributeValue.append(aPage.backgroundMusic)

        self.attributeList.append("backgroundMusicLoops")
        self.attributeValue.append(aPage.backgroundMusicLoops)

        self.attributeList.append("victory")
        self.attributeValue.append(aPage.victory)

        self.attributeList.append("death")
        self.attributeValue.append(aPage.death)

        return

    def SavePageAttributeChange(self, attribute, newValue):
        if attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "creationDate":
            self.selectedObject.creationDate = newValue
        elif attribute == "title":
            self.selectedObject.title = newValue
        elif attribute == "comment":
            self.selectedObject.comment = newValue
        elif attribute == "isFirstPage":
            self.selectedObject.isFirstPage = self.getEnteredBoolean(newValue)
        elif attribute == "backgroundImage":
            self.selectedObject.backgroundImage = newValue
        elif attribute == "backgroundMusic":
            self.selectedObject.backgroundMusic = newValue
        elif attribute == "backgroundMusicLoops":
            self.selectedObject.backgroundMusicLoops = self.getEnteredBoolean(newValue)
        elif attribute == "victory":
            self.selectedObject.victory = self.getEnteredBoolean(newValue)
        elif attribute == "death":
            self.selectedObject.death = self.getEnteredBoolean(newValue)

        return

    def FillGridWithPageChoice(self):

        aPageChoice = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(aPageChoice.ID)

        self.attributeList.append("shortText")
        self.attributeValue.append(aPageChoice.shortText)

        self.attributeList.append("longText")
        self.attributeValue.append(aPageChoice.longText)

        self.attributeList.append("reachedPageID")
        self.attributeValue.append(aPageChoice.reachedPageID)

        self.attributeList.append("requiredObjectID")
        self.attributeValue.append(aPageChoice.requiredObjectID)

        return

    def SavePageChoiceAttributeChange(self, attribute, newValue):

        if attribute == "shortText":
            self.selectedObject.shortText = newValue
        elif attribute == "longText":
            self.selectedObject.longText = newValue
        elif attribute == "reachedPageID":
            self.selectedObject.reachedPageID = newValue
        elif attribute == "requiredObjectID":
            self.selectedObject.requiredObjectID = newValue
        return

    def FillGridWithObject(self):
        anObject = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(anObject.ID)

        self.attributeList.append("author")
        self.attributeValue.append(anObject.author)

        self.attributeList.append("name")
        self.attributeValue.append(anObject.name)

        self.attributeList.append("comment")
        self.attributeValue.append(anObject.comment)

        self.attributeList.append("image")
        self.attributeValue.append(anObject.image)

        return

    def SaveObjectAttributeChange(self, attribute, newValue):
        if attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "name":
            self.selectedObject.name = newValue
        elif attribute == "comment":
            self.selectedObject.comment = newValue
        elif attribute == "image":
            self.selectedObject.image = newValue
        return

    def FillGridWithMonster(self):
        anObject = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(anObject.ID)

        self.attributeList.append("author")
        self.attributeValue.append(anObject.author)

        self.attributeList.append("name")
        self.attributeValue.append(anObject.name)

        self.attributeList.append("description")
        self.attributeValue.append(anObject.description)

        self.attributeList.append("race")
        self.attributeValue.append(anObject.race)

        self.attributeList.append("origin")
        self.attributeValue.append(anObject.origin)

        self.attributeList.append("image")
        self.attributeValue.append(anObject.image)

        self.attributeList.append("height")
        self.attributeValue.append(anObject.height)

        self.attributeList.append("lifePoints")
        self.attributeValue.append(anObject.lifePoints)

        self.attributeList.append("strength")
        self.attributeValue.append(anObject.strength)

        self.attributeList.append("agility")
        self.attributeValue.append(anObject.agility)

        self.attributeList.append("resistance")
        self.attributeValue.append(anObject.resistance)

        self.attributeList.append("recovery")
        self.attributeValue.append(anObject.recovery)

        return


    def SaveMonsterAttributeChange(self, attribute, newValue):
        if attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "name":
            self.selectedObject.name = newValue
        elif attribute == "description":
            self.selectedObject.description = newValue
        elif attribute == "race":
            self.selectedObject.race = newValue
        elif attribute == "origin":
            self.selectedObject.origin = newValue
        elif attribute == "image":
            self.selectedObject.image = newValue
        elif attribute == "height":
            self.selectedObject.height = self.getEnteredFloat(newValue)
        elif attribute == "lifePoints":
            self.selectedObject.lifePoints = self.getEnteredFloat(newValue)
        elif attribute == "strength":
            self.selectedObject.strength = self.getEnteredFloat(newValue)
        elif attribute == "agility":
            self.selectedObject.agility = self.getEnteredFloat(newValue)
        elif attribute == "resistance":
            self.selectedObject.resistance = self.getEnteredFloat(newValue)
        elif attribute == "recovery":
            self.selectedObject.recovery = self.getEnteredFloat(newValue)
        return


    def FillGridWithEnigm(self):
        anEnigm = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(anEnigm.ID)

        self.attributeList.append("author")
        self.attributeValue.append(anEnigm.author)

        self.attributeList.append("title")
        self.attributeValue.append(anEnigm.title)

        self.attributeList.append("comment")
        self.attributeValue.append(anEnigm.comment)

        return


    def SaveEnigmAttributeChange(self, attribute, newValue):
        if attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "title":
            self.selectedObject.title = newValue
        elif attribute == "comment":
            self.selectedObject.comment = newValue
        return


    def FillGridWithPossibleHero(self):
        aHero = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("ID")
        self.attributeValue.append(aHero.ID)

        self.attributeList.append("author")
        self.attributeValue.append(aHero.author)

        self.attributeList.append("name")
        self.attributeValue.append(aHero.name)

        self.attributeList.append("description")
        self.attributeValue.append(aHero.description)

        self.attributeList.append("race")
        self.attributeValue.append(aHero.race)

        self.attributeList.append("origin")
        self.attributeValue.append(aHero.origin)

        self.attributeList.append("image")
        self.attributeValue.append(aHero.image)

        self.attributeList.append("height")
        self.attributeValue.append(aHero.height)

        self.attributeList.append("lifePoints")
        self.attributeValue.append(aHero.lifePoints)

        self.attributeList.append("strength")
        self.attributeValue.append(aHero.strength)

        self.attributeList.append("resistance")
        self.attributeValue.append(aHero.resistance)

        self.attributeList.append("agility")
        self.attributeValue.append(aHero.agility)

        self.attributeList.append("recovery")
        self.attributeValue.append(aHero.recovery)

        return

    def SavePossibleHeroAttributeChange(self, attribute, newValue):
        if attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "name":
            self.selectedObject.name = newValue
        elif attribute == "description":
            self.selectedObject.description = newValue
        elif attribute == "race":
            self.selectedObject.race = newValue
        elif attribute == "origin":
            self.selectedObject.origin = newValue
        elif attribute == "image":
            self.selectedObject.image = newValue
        elif attribute == "height":
            self.selectedObject.height = self.getEnteredFloat(newValue)
        elif attribute == "lifePoints":
            self.selectedObject.lifePoints = self.getEnteredFloat(newValue)
        elif attribute == "strength":
            self.selectedObject.strength = self.getEnteredFloat(newValue)
        elif attribute == "resistance":
            self.selectedObject.resistance = self.getEnteredFloat(newValue)
        elif attribute == "agility":
            self.selectedObject.agility = self.getEnteredFloat(newValue)
        elif attribute == "recovery":
            self.selectedObject.recovery = self.getEnteredFloat(newValue)
        return

    def FillGridWithBook(self):
        aBook = self.selectedObject

        self.attributeList = list()
        self.attributeValue = list()

        self.attributeList.append("creationDate")
        self.attributeValue.append(aBook.creationDate)

        self.attributeList.append("author")
        self.attributeValue.append(aBook.author)

        self.attributeList.append("title")
        self.attributeValue.append(aBook.title)

        self.attributeList.append("shortDescription")
        self.attributeValue.append(aBook.shortDescription)

        self.attributeList.append("splashScreenAsset")
        self.attributeValue.append(aBook.splashScreenAsset)

        return


    def SaveBookAttributeChange(self, attribute, newValue):
        if attribute == "creationDate":
            self.selectedObject.creationDate = newValue
        elif attribute == "author":
            self.selectedObject.author = newValue
        elif attribute == "title":
            self.selectedObject.title = newValue
        elif attribute == "shortDescription":
            self.selectedObject.shortDescription = newValue
        elif attribute == "splashScreenAsset":
            self.selectedObject.splashScreenAsset = newValue
        return




# todo JRA Add functions for other object type Monsters, Objects, Enigms to fill with attributes then save attributes
# todo based on  FillGridWithPageChoice() and FillGridWithPageChoice()
