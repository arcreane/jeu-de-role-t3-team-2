import pickle

import Book
import CurrentHero


class CurrentGame:

    def __init__(self):
        self.book = Book.Book()                # the book that is played
        self.theCurrentHero = CurrentHero.CurrentHero()  # the current hero that is playing
        self.lastPageID = ''                # the ID of the last page (for instance is we fail an enigm a combat we need to be able to go back !
        self.currentPageID = ''             # the ID of the current page played
        return

    def saveCurrentGame(self, currentGamesPath, mainFilename):
        pickle.dump(self, mainFilename)
        return

    def loadCurrentGame(self, currentGamesPath, mainFilename):
        self = pickle.load(mainFilename)
        return

