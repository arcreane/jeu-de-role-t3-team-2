import pickle

import Page
import datetime as dt


class Book:

    # __init__ : Book instance initialization function : reset all members and create an ID using date time functions
    def __init__(self, bookTitle="New Book"):
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S")            # book creation date
        self.author = ''                  # free string entered by the author in design mode
        self.splashScreenAsset = ''        # filename of book image asset to display as a splash screen while starting
        self.title = bookTitle            # title of the book (used to store main data within title.book file
        self.shortDescription = ''        # short description to let the user select the book he wants to play
        self.narrative = ''               # displayed to the user when starting to play to place the context of the book "once upon a time ..."
        self.pages=dict()                 # dictionnary that store the pages ( objects of class Page)
        self.possibleHeros=dict()         # dictionnary that store the possible heros (objects of class PossibleHero)
        return

    def saveBook(self, booksPath, fileForSave):     # Function to be called to save the designed book in path 'booksPath', using 'fileForSave' file
        pickle.dump(self, fileForSave)
        return

    def loadBook(self, booksPath, fileForLoad):     # Function to be called in designer or player to load a book
        self = pickle.load(fileForLoad)
        return self

    def getFirstPageID(self):                       # return a page instance that is the 1st First page as a root of the designer treeview, as a first page when starting to play the game
        for page in self.pages:                     # loop over pages of the book in dictionary pages
            if self.pages[page].isFirstPage:            # if this page isFirstPAge return its ID
                return self.pages[page].ID
        return ""

    def addPageToBook(self, aPage):                 # add a Page 'aPage' in the dictionary of pages
        if aPage.ID not in self.pages:              # if pageID is not already in the book 'pages' (avoid twice same page)
            self.pages[aPage.ID]=aPage                  # then add it to the dictionary of pages
        return

    def deletePageOfBook(self, aPage):              #delete a page of the dictionary of pages
        if aPage.ID in self.pages:                  # if the page is in the book
            self.pages.pop(aPage.ID)                    # then delete (pop to delete dictionary entry in python) it from dictionary of pages
        return

    def addPossibleHeroToBook(self, aPossibleHero):     # comparable as 2 above functions with other dictionary : 'possibleHeros'
        if aPossibleHero.ID not in self.possibleHeros:
            self.possibleHeros[aPossibleHero.ID] = aPossibleHero
        return

    def deletePossibleHeroOfBook(self, aPossibleHero):
        if aPossibleHero.ID in self.possibleHeros:
            self.possibleHeros.pop(aPossibleHero.ID)
        return

    def getPageFromID(self, searchedID):
        ret = None
        for page in self.pages:
            if page == searchedID:
                ret = self.pages[page]
        return ret

    def getPageChoiceFromID(self, searchedID):
        ret = None
        for page in self.pages:
            thePage = self.pages[page]
            if len(thePage.choices) > 0:
                for pc in thePage.choices:
                    if pc == searchedID:
                        ret = thePage.choices[pc]
        return ret

    def getObjectFromID(self, searchedObjID):
        ret = None
        for page in self.pages:
            thePage = self.pages[page]
            if len(thePage.objects) > 0:
                for obj in thePage.objects:
                    if obj == searchedObjID:
                        ret = thePage.objects[obj]
        return ret

    def getMonsterFromID(self, searchedMonsterID):
        ret = None
        for page in self.pages:
            thePage = self.pages[page]
            if len(thePage.monsters) > 0:
                for monster in thePage.monsters:
                    if monster == searchedMonsterID:
                        ret = thePage.monsters[monster]
        return ret

    def getEnigmFromID(self, searchedEnigmID):
        ret = None
        for page in self.pages:
            thePage = self.pages[page]
            if len(thePage.enigms) > 0:
                for enigm in thePage.enigms:
                    if enigm == searchedEnigmID:
                        ret = thePage.enigms[enigm]
        return ret

    def getPossibleHeroFromID(self, searchHeroID):
        ret = None
        for hero in self.possibleHeros:
            theHero = self.possibleHeros[hero]
            if theHero.ID == searchHeroID:
                ret = theHero
        return ret

    def getPagesChoiceList(self):
        ret = list()
        for page in self.pages:
            ret.append(page.ID)
        return ret

    def getAllpagesList(self):
        retValue = list()
        for page in self.pages:
            retValue.append(self.pages[page].getDisplayedText())
        return retValue

    def getPageIDFromDisplayedText(self, displayedText):
        retValue = ''
        for page in self.pages:
            if self.pages[page].getDisplayedText() == displayedText:
                retValue = self.pages[page].ID
        return retValue

# todo JRA Add other 'get' functions from book to get Monsters, Objects, Enigms from their ID
# todo based on  getPageChoiceFromID()



# ID will be unique and be used for treeview, verification, game
# dictionary in our case implies unique IDs inserted in dictionaries
# that's why it is tested prior insertion of new object in a dictionary
