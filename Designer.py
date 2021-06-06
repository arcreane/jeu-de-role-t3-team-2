import copy
import ntpath

import Book
import HB_Utilities
import Page
import Hero
import CheckGameValidity
import PageChoice
import TreeviewProperty
import Splash
import Object
import Monster
import Enigm

import os

import tkinter as tk  # TkInter package is imported and is referred below as "tk."
import tkinter.ttk

from tkinter.filedialog import asksaveasfile    # filedialog = tkinter dialogboxes # asksaveasfile = choose file to save data
from tkinter.filedialog import askopenfilename  # idem for load
from tkinter import messagebox                  # idem for Yes/No/Cancel messageboxes

import mboxEnterText

from shutil import copyfile


BACK_COLOR = 'lightgrey'
BASE_TITLE = " HeroBook Designer - "
MAX_ENIGM_ANSWER = 10


class Designer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):  # contructor of a python class
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.currentFileName = "NewBook"
        self.hasUnsavedChanges = None
        self.pagesTreeview = None
        self.pagesTreeviewLastSelectedItem =''          # Store ID of last selected item in treeview (if it changes update right part)
        self.bookValidityLabel = None
        self.book = None
        self.popupBook = None
        self.popupPage = None
        self.popupPossibleHeroes = None
        self.popupEnigm = None
        self.popupPageChoice = None
        self.popupObject = None
        self.popupMonster = None
        self.popupHero = None
        self.popupAnswer = None
        self.treeviewLastClickedItem = None
        self.treeviewProperty = None
        self.textEntry = None
        self.nextIndexToUse = 0

        self.BuildWindowLayout()
        self.NewGame()
        return

    def AboutBox(self):
        print('About')  # for test now ...
        return

    def CheckIfSavedDone(self):
        if self.hasUnsavedChanges:
            ret = tk.messagebox.askyesnocancel(
                title="Save Changes ...",
                message='Do you want to save changes before loosing them ?',
                default=tk.messagebox.YES,
                parent=self)
            if ret:                     # Yes
                self.SaveGame()
                return True
            elif ret is None:           # Cancel
                return False
            else:                       # No
                return True
        return True

    def NewGame(self):
        hasSucceeded = False
        if self.CheckIfSavedDone():
            hasSucceeded = True
            print('NewGame')  # for test now ...
            self.book = Book.Book()
            self.hasUnsavedChanges = False
            self.refreshWindow()
        return hasSucceeded

    def OpenGame(self):
        hasSucceeded = False
        if self.NewGame():
            hasSucceeded = True
            print('LoadGame')  # for test now ...
            name = askopenfilename(initialdir="./Books", filetypes=[("Hero books", "*.HeroBook")], title="Choose a Hero Book to open ...", parent=self)
            try:
                with open(name, 'rb') as f:
                    self.book = self.book.loadBook('.', f)
                    f.close()
                self.hasUnsavedChanges = False
                self.refreshWindow()

            except:
                print("No file exists")
                hasSucceeded = False
        return hasSucceeded

    def SaveGame(self):
        hasSucceeded = True
        print('SaveGame')  # for test now in final version it should create a directory for the game, move assets here, change assets path in assets ... then keep the save below
        f = asksaveasfile(mode='wb', initialdir="./Books", filetypes=[("Hero Books", "*.HeroBook")], defaultextension=".HeroBook", title="Choose a filename to save your Hero Book ...", parent=self)
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            hasSucceeded = False
            return
        try:
            self.currentFileName = os.path.basename(f.name)
            self.book.saveBook('.', f)
            f.close()  # `()` was missing.
            self.hasUnsavedChanges = False
            self.refreshWindow()
            pass
        except:
            hasSucceeded = False
        return hasSucceeded

    def QuitDesigner(self):
        hasSucceeded = False
        if self.CheckIfSavedDone():
            hasSucceeded = True
            print('QuitDesigner')  # for test now ...
            self.parent.destroy()
        return hasSucceeded

    def BuildMenu(self):

        menuBar = tk.Menu(self.parent)  # menuBar is the container of the menu in the window
        self.parent['menu'] = menuBar  # we attach it to the window
        subMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label='Game', menu=subMenu)
        subMenu.add_command(label='New', command=self.NewGame)
        subMenu.add_separator()
        subMenu.add_command(label='Save', command=self.SaveGame)
        subMenu.add_command(label='Open', command=self.OpenGame)
        subMenu.add_separator()
        subMenu.add_command(label='Export book', command=self.ExportGame)
        subMenu.add_separator()
        subMenu.add_command(label='Quit', command=self.QuitDesigner)
        self.createTreeviewContextMenus()
        return

    def createTreeviewContextMenus(self):
        self.popupBook = tk.Menu(self.parent, tearoff=0)
        self.popupBook.add_command(label="Add page", command=self.OnMenuBookAddPage)
        self.popupBook.add_separator()
        self.popupBook.add_command(label="Close popup menu")

        self.popupEnigm = tk.Menu(self.parent, tearoff=0)
        self.popupEnigm.add_command(label="Add Good answer", command=self.OnMenuEnigmAddGoodAnswer)
        self.popupEnigm.add_command(label="Add bad answer", command=self.OnMenuEnigmAddBadAnswer)
        self.popupEnigm.add_separator()
        self.popupEnigm.add_command(label="Delete enigm", command=self.OnMenuDeleteItem)
        self.popupEnigm.add_separator()
        self.popupEnigm.add_command(label="Close popup menu")

        self.popupPageChoice = tk.Menu(self.parent, tearoff=0)
        self.popupPageChoice.add_command(label="Delete page choice", command=self.OnMenuDeleteItem)
        self.popupPageChoice.add_separator()
        self.popupPageChoice.add_command(label="Close popup menu")

        self.popupObject = tk.Menu(self.parent, tearoff=0)
        self.popupObject.add_command(label="Delete object", command=self.OnMenuDeleteItem)
        self.popupObject.add_separator()
        self.popupObject.add_command(label="Close popup menu")

        self.popupMonster = tk.Menu(self.parent, tearoff=0)
        self.popupMonster.add_command(label="Delete monster", command=self.OnMenuDeleteItem)
        self.popupMonster.add_separator()
        self.popupMonster.add_command(label="Close popup menu")

        self.popupHero = tk.Menu(self.parent, tearoff=0)
        self.popupHero.add_command(label="Delete hero", command=self.OnMenuDeleteItem)
        self.popupHero.add_separator()
        self.popupHero.add_command(label="Close popup menu")

        self.popupAnswer = tk.Menu(self.parent, tearoff=0)
        self.popupAnswer.add_command(label="Delete answer of enigm", command=self.OnMenuDeleteItem)
        self.popupAnswer.add_separator()
        self.popupAnswer.add_command(label="Close popup menu")

        self.popupPage = tk.Menu(self.parent, tearoff=0)
        self.popupPage.add_command(label="Add PageChoice", command=self.OnMenuPageAddPageChoice)
        self.popupPage.add_command(label="Add Object", command=self.OnMenuPageAddObject)
        self.popupPage.add_command(label="Add Monster", command=self.OnMenuPageAddOMonster)
        self.popupPage.add_command(label="Add Enigm", command=self.OnMenuPageAddEnigm)
        self.popupPage.add_separator()
        self.popupPage.add_command(label="Delete page", command=self.OnMenuDeleteItem)
        self.popupPage.add_separator()
        self.popupPage.add_command(label="Close popup menu")

        self.popupPossibleHeroes = tk.Menu(self.parent, tearoff=0)
        self.popupPossibleHeroes.add_command(label="Add Hero", command=self.OnMenuPossibleHeroAddHero)
        self.popupPossibleHeroes.add_separator()
        self.popupPossibleHeroes.add_command(label="Close popup menu")

        return

    def BuildWindowLayout(self):
        self.parent.wm_state('zoomed')  # use python function 'wm_state' to change current window state to maximized

        frame_leftPane = tk.Frame(master=self, width=400)  # Left Frame in main window
        frame_rightPane = tk.Frame(master=self, width=300)  # Right Frame in main window

        treeViewPane = tk.Frame(master=frame_leftPane, width=400, height=300, relief=tk.GROOVE, borderwidth=1,
                                bg=BACK_COLOR)
        validityPane = tk.Frame(master=frame_leftPane, width=400, height=100, relief=tk.GROOVE, borderwidth=1,
                                bg=BACK_COLOR)

        propertyPane = tk.Frame(master=frame_rightPane, width=300, height=200, relief=tk.GROOVE, borderwidth=1,
                                bg=BACK_COLOR)
        overViewPane = tk.Frame(master=frame_rightPane, width=300, height=200, relief=tk.GROOVE, borderwidth=1,
                                bg=BACK_COLOR)

        self.pagesTreeview = tk.ttk.Treeview(master=treeViewPane)
        self.pagesTreeview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.pagesTreeview.bind("<Button-1>", self.treeviewLeftClick)
        self.pagesTreeview.bind("<Button-3>", self.treeviewRightClick)
        self.pagesTreeview.bind('<<TreeviewSelect>>', self.treeviewSelectionChanged)

        self.bookValidityLabel = tk.ttk.Label(master=validityPane)
        self.bookValidityLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.treeviewProperty = TreeviewProperty.TreeviewProperty(self.parent, propertyPane, self.book)
        self.treeviewProperty.pack(fill="both", expand=True)

        # tk.Frame.Pack is the function to indicate to tkinter that thee frame must be resized when parent size changes
        treeViewPane.pack(side=tk.TOP, fill=tk.BOTH,
                          expand=True)  # indicate how the pane is attached to its parent during resizing
        validityPane.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  # side = indicate side of attachment
        propertyPane.pack(side=tk.TOP, fill=tk.BOTH,
                          expand=True)  # fill = indicate direction of expansion (X, Y, or Both)
        overViewPane.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  # expand ) indicates if expansion is possible

        frame_leftPane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_rightPane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.BuildMenu()

        return

    def open_treeviewChildren(self, parent):
        self.pagesTreeview.item(parent, open=True)
        for child in self.pagesTreeview.get_children(parent):
            self.open_treeviewChildren(child)
        return

    def refreshWindow(self):
        # empty the treeview
        self.pagesTreeview.delete(*self.pagesTreeview.get_children())

        # ensure that the property page object is referring to the right opened book !
        self.treeviewProperty.book = self.book


        # add pages
        self.pagesTreeview.insert("", 0, "Book", text="Book")
        print('Inserting Book')

        # add the 1st first page we find
        self.nextIndexToUse = 1
        firstPageID = self.book.getFirstPageID()
        if firstPageID != "":
            theFirstPage = self.book.pages[firstPageID]
            self.ContinueBookInsertionInTreeview("Book", theFirstPage)

        # add the eventual orphan pages not already in the treeview following the 1st first page
        for page in self.book.pages:
            if not self.pagesTreeview.exists(self.book.pages[page].ID):
                self.ContinueBookInsertionInTreeview("Book", self.book.pages[page])

        # add possible heroes
        self.nextIndexToUse = 10001
        self.pagesTreeview.insert("", self.nextIndexToUse, "Heroes", text="Heroes")
        print('Inserting Heroes')
        self.nextIndexToUse += 1

        for hero in self.book.possibleHeros:
            theHero = self.book.possibleHeros[hero]
            self.pagesTreeview.insert("Heroes", self.nextIndexToUse, theHero.ID, text=theHero.ID + " : " + theHero.name)
            print('Inserting Hero : '+theHero.ID)
            self.nextIndexToUse += 1
        self.open_treeviewChildren(self.pagesTreeview.focus())

        # refresh title of main window with application name, bookfilename, and a star (*) if there are unsaved changes
        windowTitle = BASE_TITLE + self.currentFileName
        if self.hasUnsavedChanges:
            windowTitle = windowTitle+" *"
        self.parent.title(windowTitle)

        self.bookValidityLabel.config(text=str(CheckGameValidity.checkValidity(self.book)))

        return

    def ContinueBookInsertionInTreeview(self, parentNodeID, aPage):
        # Insert page in treeview if not existing
        if not self.pagesTreeview.exists(aPage.ID):
            self.pagesTreeview.insert(parentNodeID, self.nextIndexToUse, aPage.ID, text=aPage.ID + " : " + aPage.title)
            print('Inserting Page : ' + aPage.ID)
            self.nextIndexToUse += 1

            # Insert eventual objects in treeview (if not already existing)
            for obj in aPage.objects:
                theObj = aPage.objects[obj]
                if not self.pagesTreeview.exists(theObj.ID):
                    self.pagesTreeview.insert(aPage.ID, self.nextIndexToUse, theObj.ID,
                                              text=theObj.ID + " : " + theObj.name)
                    print('Inserting Object : ' + theObj.ID)
                    self.nextIndexToUse += 1

            # Insert eventual enigms in treeview (if not already existing)
            for enigm in aPage.enigms:
                theEnigm = aPage.enigms[enigm]
                if not self.pagesTreeview.exists(theEnigm.ID):
                    self.pagesTreeview.insert(aPage.ID, self.nextIndexToUse, theEnigm.ID,
                                              text=theEnigm.ID + " : " + theEnigm.title)
                    print('Inserting Enigm : ' + theEnigm.ID)
                    self.nextIndexToUse += 1
                    # insert eventual answers
                    for ans in theEnigm.possibleAnswers:
                        self.pagesTreeview.insert(theEnigm.ID, self.nextIndexToUse, ans + theEnigm.ID,
                                                  text=theEnigm.possibleAnswers[ans] + " : " + str(theEnigm.goodAnswers[ans]))
                        print('Inserting answer : ' + ans + theEnigm.ID)
                        self.nextIndexToUse += 1

            # Insert eventual monsters in treeview (if not already existing)
            for monster in aPage.monsters:
                theMonster = aPage.monsters[monster]
                if not self.pagesTreeview.exists(theMonster.ID):
                    self.pagesTreeview.insert(aPage.ID, self.nextIndexToUse, theMonster.ID,
                                              text=theMonster.ID + " : " + theMonster.name)
                    print('Inserting Monster : ' + theMonster.ID)
                    self.nextIndexToUse += 1

            # Insert enventual pages choice (then potentially reinsert pages)
            for aPageChoiceID in aPage.choices:
                aPageChoice = aPage.choices[aPageChoiceID]
                self.pagesTreeview.insert(aPage.ID, self.nextIndexToUse, aPageChoice.ID,
                                          text=aPageChoice.ID + " : " + aPageChoice.shortText)
                print('Inserting Page Choice : ' + aPageChoice.ID)
                self.nextIndexToUse += 1
                if aPageChoice.reachedPageID != '':
                    nextPage = self.book.getPageFromID(aPageChoice.reachedPageID)
                    if nextPage is not None:
                        self.ContinueBookInsertionInTreeview(aPageChoice.ID, nextPage)
        else:
            print("PageID is looping: ", aPage.ID)
        return

    def treeviewSelectionChanged(self, event):
        curItem = self.pagesTreeview.focus()
        self.pagesTreeview.item(curItem)
        print('selection changed:', event, self.pagesTreeview.item(curItem))
        self.pagesTreeviewLastSelectedItem=curItem
        self.treeviewProperty.EmptyContent()
        if len (curItem) > 0 :
            # detect selected object type
            objetType=curItem[0:2]
            if objetType == '_P' :  # It's a page
                thePage = self.book.getPageFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, thePage)
            elif objetType == "PC":  # It's a Page Choice
                thePageChoice = self.book.getPageChoiceFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, thePageChoice)
            elif objetType == "_O":  # It is an object
                theObject = self.book.getObjectFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, theObject)
            elif objetType == "_M":  # It is a monster
                theMonster = self.book.getMonsterFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, theMonster)
            elif objetType == "_E":  # It is an Enigm
                theEnigm = self.book.getEnigmFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, theEnigm)
            elif objetType == "_H":  # It is a Possible Hero
                theHero = self.book.getPossibleHeroFromID(curItem)
                self.treeviewProperty.SelectionChanged(curItem, theHero)
            elif objetType == "Bo":  # It is the book
                self.treeviewProperty.SelectionChanged(curItem, self.book)
            return
        return

    def treeviewLeftClick(self, event):
        treeviewLastClickedItem = self.pagesTreeview.identify_row(event.y)
        print('Left clicked item:', treeviewLastClickedItem)
        # if selection change, refresh property window to the right
        self.pagesTreeviewLastSelectedItem = treeviewLastClickedItem
        return

    def treeviewRightClick(self, event):
        treeviewLastClickedItem = self.pagesTreeview.identify_row(event.y)
        print('Right clicked item:', treeviewLastClickedItem)
        self.pagesTreeviewLastSelectedItem = treeviewLastClickedItem
        thePopupToUse = None
        if treeviewLastClickedItem == 'Book':
            thePopupToUse = self.popupBook
        elif treeviewLastClickedItem == 'Heroes':
            thePopupToUse = self.popupPossibleHeroes
        elif treeviewLastClickedItem[0:2] == '_P':
            thePopupToUse = self.popupPage
        elif treeviewLastClickedItem[0:2] == '_E':
            thePopupToUse = self.popupEnigm
        elif treeviewLastClickedItem[0:2] == 'PC':
            thePopupToUse = self.popupPageChoice

        elif treeviewLastClickedItem[0:2] == '_O':
            thePopupToUse = self.popupObject
        elif treeviewLastClickedItem[0:2] == '_M':
            thePopupToUse = self.popupMonster
        elif treeviewLastClickedItem[0:2] == '_H':
            thePopupToUse = self.popupHero
        elif treeviewLastClickedItem[0:2] == 'AN':
            thePopupToUse = self.popupAnswer
        else:
            pass
        if thePopupToUse is not None:
            try:
                thePopupToUse.tk_popup(event.x_root, event.y_root, 0)
            finally:
                thePopupToUse.grab_release()
        return

    def OnMenuBookAddPage(self):
        theNewPage = Page.Page()
        theNewPage.isFirstPage = True
        self.book.addPageToBook(theNewPage)
        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(theNewPage.ID)
        self.pagesTreeview.focus(theNewPage.ID)
        return

    def OnMenuPageAddPageChoice(self):
        thePageChoice = PageChoice.PageChoice()
        thePage = self.book.pages[self.pagesTreeviewLastSelectedItem]
        if thePageChoice.ID not in thePage.choices:              # if pageID is not already in the book 'pages' (avoid twice same page)
            if len(thePage.choices)<5:
                thePage.choices[thePageChoice.ID]=thePageChoice
            else:
                tk.messagebox.showerror(master=self.parent, title="Too many ...", message="Page choices limited to max 5 !")

        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(thePageChoice.ID)
        self.pagesTreeview.focus(thePageChoice.ID)
        return

    def OnMenuEnigmAddGoodAnswer(self):
        return self.OnMenuEnigmAddAnswer(True)

    def OnMenuEnigmAddBadAnswer(self):
        return self.OnMenuEnigmAddAnswer(False)

    def OnMenuEnigmAddAnswer(self, isGoodAnswer):

        enigmID = self.pagesTreeviewLastSelectedItem
        theEnigm = self.book.getEnigmFromID(enigmID)
        self.textEntry = mboxEnterText.mboxEnterTextPopupWindow(self.parent)
        self.parent.wait_window(self.textEntry.top)
        try:
            print(self.textEntry.value)
            # todo jra : bug ==> if answer is deleted then reinserted ANx could be already used
            newAnswerNb = None
            for i in range(MAX_ENIGM_ANSWER):
                if ('AN'+str(i)) not in theEnigm.possibleAnswers:
                    newAnswerNb = i
                    break
            if newAnswerNb is not None:
                key = 'AN' + str(newAnswerNb)
                theEnigm.possibleAnswers[key] = self.textEntry.value
                theEnigm.goodAnswers[key] = isGoodAnswer
                self.hasUnsavedChanges = True
                self.refreshWindow()
        except:
            print ('cancelled')
            pass

        return

    def OnMenuPageAddObject(self):
        theObject = Object.Object()
        thePage = self.book.pages[self.pagesTreeviewLastSelectedItem]
        if theObject.ID not in thePage.objects:  # if objectID is not already in the book 'objects' (avoid twice same page)
            thePage.objects[theObject.ID] = theObject
        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(theObject.ID)
        self.pagesTreeview.focus(theObject.ID)
        return

    def OnMenuPageAddOMonster(self):
        theMonster = Monster.Monster()
        thePage = self.book.pages[self.pagesTreeviewLastSelectedItem]
        if theMonster.ID not in thePage.monsters:  # if monster.ID is not already in the page 'monsters' (avoid twice same monster)
            thePage.monsters[theMonster.ID] = theMonster
        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(theMonster.ID)
        self.pagesTreeview.focus(theMonster.ID)
        return

    def OnMenuPageAddEnigm(self):
        theEnigm = Enigm.Enigm()
        thePage = self.book.pages[self.pagesTreeviewLastSelectedItem]
        if theEnigm.ID not in thePage.enigms:  # if monster.ID is not already in the page 'monsters' (avoid twice same monster)
            thePage.enigms[theEnigm.ID] = theEnigm
        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(theEnigm.ID)
        self.pagesTreeview.focus(theEnigm.ID)
        return

    def OnMenuPossibleHeroAddHero(self):
        theHero = Hero.Hero()
        if theHero.ID not in self.book.possibleHeros:  # if monster.ID is not already in the page 'monsters' (avoid twice same monster)
            self.book.possibleHeros[theHero.ID] = theHero
        self.hasUnsavedChanges = True
        self.refreshWindow()
        self.pagesTreeview.selection_set(theHero.ID)
        self.pagesTreeview.focus(theHero.ID)
        return

    def OnMenuDeleteItem(self):
        if HB_Utilities.AreYouSure(self.parent, "Sure ?", "Are you sure you want to permanently delete this item. This action cannot be undo !"):
            lastSelectedID = self.pagesTreeviewLastSelectedItem
            objType = lastSelectedID[0:2]
            if objType == '_P':
                thePage = self.book.pages[lastSelectedID]
                if thePage is not None:
                    # delete references in page choices
                    for page in self.book.pages:
                        thePage = self.book.pages[page]
                        for pageChoice in thePage.choices:
                            thePageChoice = thePage.choices[pageChoice]
                            if thePageChoice.reachedPageID == lastSelectedID:
                                thePageChoice.reachedPageID = ''

                    # remove page from book
                    self.book.pages.pop(lastSelectedID)
                    # say needs to be saved
                    self.hasUnsavedChanges = True
                    # refresh window
                    self.refreshWindow()
                    # set focus on parent Page
                    self.pagesTreeview.selection_set('Book')
                    self.pagesTreeview.focus('Book')


            elif objType == '_E':
                # find page of enigm
                thePage = None
                for page in self.book.pages:
                    if lastSelectedID in self.book.pages[page].enigms:
                        thePage=self.book.pages[page]
                if thePage is not None:
                    # remove enigm from list or enigms
                    thePage.enigms.pop(lastSelectedID)
                    # say needs to be saved
                    self.hasUnsavedChanges = True
                    # refresh window
                    self.refreshWindow()
                    # set focus on parent Page
                    self.pagesTreeview.selection_set(thePage.ID)
                    self.pagesTreeview.focus(thePage.ID)
            elif objType == 'PC':
                thePageToSelect = None
                for page in self.book.pages:
                    thePage = self.book.pages[page]
                    if lastSelectedID in thePage.choices:
                        for pageChoice in thePage.choices:
                            if pageChoice == lastSelectedID:
                                thePageToSelect = page
                        thePage.choices.pop(lastSelectedID)
                # say needs to be saved
                self.hasUnsavedChanges = True
                # refresh window
                self.refreshWindow()
                # set focus on parent Page
                self.pagesTreeview.selection_set(thePageToSelect)
                self.pagesTreeview.focus(thePageToSelect)
            elif objType == '_O':
                # find page of object
                thePage = None
                for page in self.book.pages:
                    if lastSelectedID in self.book.pages[page].objects:
                        thePage = self.book.pages[page]
                if thePage is not None:
                    # remove object from dict of objects
                    thePage.objects.pop(lastSelectedID)
                    # say needs to be saved
                    self.hasUnsavedChanges = True
                    # refresh window
                    self.refreshWindow()
                    # set focus on parent Page
                    self.pagesTreeview.selection_set(thePage.ID)
                    self.pagesTreeview.focus(thePage.ID)
            elif objType == '_M':
                # find page of monster
                thePage = None
                for page in self.book.pages:
                    if lastSelectedID in self.book.pages[page].monsters:
                        thePage = self.book.pages[page]
                if thePage is not None:
                    # remove object from dict of objects
                    thePage.monsters.pop(lastSelectedID)
                    # say needs to be saved
                    self.hasUnsavedChanges = True
                    # refresh window
                    self.refreshWindow()
                    # set focus on parent Page
                    self.pagesTreeview.selection_set(thePage.ID)
                    self.pagesTreeview.focus(thePage.ID)
            elif objType == '_H':
                if lastSelectedID in self.book.possibleHeros:
                    self.book.possibleHeros.pop(lastSelectedID)
                    # say needs to be saved
                    self.hasUnsavedChanges = True
                    # refresh window
                    self.refreshWindow()
                    # set focus on parent Page
                    self.pagesTreeview.selection_set('Heroes')
                    self.pagesTreeview.focus('Heroes')
            elif objType == 'AN':
                # find answer ID and page ID from lastSelectedID
                splitStringTable = lastSelectedID.split('_')
                if len(splitStringTable) == 2:
                    enigmID = '_' + splitStringTable[1]
                    answerID = splitStringTable[0]
                    theEnigm = self.book.getEnigmFromID(enigmID)
                    if theEnigm is not None:
                        theEnigm.possibleAnswers.pop(answerID)
                        theEnigm.goodAnswers.pop(answerID)
                        # say needs to be saved
                        self.hasUnsavedChanges = True
                        # refresh window
                        self.refreshWindow()
                        # set focus on parent Page
                        self.pagesTreeview.selection_set(theEnigm.ID)
                        self.pagesTreeview.focus(theEnigm.ID)

        return

    def ExportGame(self):
        # ask user to select a export game name
        ret = False
        initialDir = os.path.abspath('./Books/')
        returnFromDialog = tk.filedialog.askdirectory(parent=self, initialdir=initialDir, title='Select folder to export the book ...', mustexist=tk.TRUE)
        print(returnFromDialog)
        returnFromDialog = os.path.abspath(returnFromDialog)
        if returnFromDialog != '' and os.path.isdir(returnFromDialog) and returnFromDialog != initialDir:
            ret = True
            # if folder exist, confirm it will be erased and lost
            targetPath = returnFromDialog
            if HB_Utilities.AreYouSure(self, 'Are you sure ?', 'All data in "' + targetPath + '" folder will be erased. Are you sure you want to proceed ?'):
                # erase target folder data
                if HB_Utilities.EraseFolderData(targetPath):
                    try:
                        # make a deep-copy of the game (because we will change path to destination before saving it)
                        exportBook = copy.deepcopy(self.book)
                        # copy current game assets in target folder
                        # copy all assets in target folder and change their path in deepcopy book
                        # try / Exception mechanism if any exception we assume overall as failed and just put a dialog box
                        # 0) book splash screen
                        if exportBook.splashScreenAsset != '':
                            sourceFilename = ntpath.basename(exportBook.splashScreenAsset)
                            targetFullFilename = os.path.join(targetPath, sourceFilename)
                            copyfile(exportBook.splashScreenAsset, targetFullFilename)
                            exportBook.splashScreenAsset = sourceFilename
                        # 1) start with pages
                        for page in exportBook.pages:
                            thePage = exportBook.pages[page]
                            # treat thePage backgroundImage
                            if thePage.backgroundImage != '':
                                sourceFilename = ntpath.basename(thePage.backgroundImage)
                                targetFullFilename = os.path.join(targetPath, sourceFilename)
                                copyfile(thePage.backgroundImage, targetFullFilename)
                                thePage.backgroundImage = sourceFilename
                            # treat thePage backgroundMusic
                            if thePage.backgroundMusic != '':
                                sourceFilename = ntpath.basename(thePage.backgroundMusic)
                                targetFullFilename = os.path.join(targetPath, sourceFilename)
                                copyfile(thePage.backgroundMusic, targetFullFilename)
                                thePage.backgroundMusic = sourceFilename
                            # treat monsters assets
                            for monster in thePage.monsters:
                                theMonster = thePage.monsters[monster]
                                if theMonster.image != '':
                                    sourceFilename = ntpath.basename(theMonster.image)
                                    targetFullFilename = os.path.join(targetPath, sourceFilename)
                                    copyfile(theMonster.image, targetFullFilename)
                                    theMonster.image = sourceFilename
                            # treat objects assets
                            for object in thePage.objects:
                                theObject = thePage.objects[object]
                                if theObject.image != '':
                                    sourceFilename = ntpath.basename(theObject.image)
                                    targetFullFilename = os.path.join(targetPath, sourceFilename)
                                    copyfile(theObject.image, targetFullFilename)
                                    theObject.image = sourceFilename
                            # No assets in enigm class
                            # No assets in page choice class
                        # 2) then possible heroes
                        for hero in exportBook.possibleHeros:
                            theHero = exportBook.possibleHeros[hero]
                            if theHero.image != '':
                                sourceFilename = ntpath.basename(theHero.image)
                                targetFullFilename = os.path.join(targetPath, sourceFilename)
                                copyfile(theHero.image, targetFullFilename)
                                theHero.image = sourceFilename

                        # pickle-save the cloned book
                        # open a target file in this folder
                        exportMainFN = os.path.join(targetPath,'Main.HeroBook')
                        with open(exportMainFN, 'wb') as f:
                            # export the target file in this folder
                            exportBook.saveBook(targetPath, f)
                            f.close()

                        # message box to say it is ok
                        HB_Utilities.OKMBox(self.parent, 'Export', 'Export successfully done !')
                        pass
                    except:
                        # message box to say it failed
                        HB_Utilities.OKMBox(self.parent, 'Export', 'Export Fails !')
                        pass
        return ret

def launchDesigner():
    theWindow = tk.Tk()  # Creation of parent widget

    theWindow.withdraw()
    theWindow.iconbitmap('./images/HeroBook.ico')
    splash = Splash.Splash(theWindow, './images/splashDesigner.gif', 3)
    Designer(theWindow).pack(side="top", fill="both", expand=True)  # creation of one instance of my class, attached to the parent and made resizeable
    theWindow.mainloop()
    return
