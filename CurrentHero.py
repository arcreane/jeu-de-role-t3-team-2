import Hero
import Object
import datetime as dt

class CurrentHero():

    def __init__(self):
        self.ID = 'CH'+dt.datetime.now().strftime("%Y%m%d %H%M%S")                        # unique ID that identifies the page
        self.author = ''                    # free string entered by the author in design mode
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S")              # page creation date
        self.possibleHeroBasedOn = Hero.Hero()   # initial hero used to start playing
        self.theLiveHero = Hero.Hero()           # copy of the initial to store live status (ie LP decreased ...)
        self.objectsInventory = dict()       # this dictionnary stores objects picked up
        return

    def addObjetToInventory(self, anObject):
        if anObject.ID not in self.objectsInventory:
            self.objectsInventory[anObject.ID] = anObject
        return

    def deleteObjectFromInventory(self, anObject):
        if anObject.ID in self.objectsInventory:
            self.objectsInventory.pop(anObject.ID)
        return


