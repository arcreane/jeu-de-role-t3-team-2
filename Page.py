import Monster
import Object
import Enigm
import PageChoice
import datetime as dt

class Page:

    def __init__(self, pageTitle="New Page"):
        self.ID = '_P'+dt.datetime.now().strftime("%Y%m%d %H%M%S")                       # unique ID that identifies the page
        self.author = ''                  # free string entered by the author in design mode
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S")            # page creation date
        self.title = pageTitle            # title of the page
        self.comment = ''                 # text written at top
        self.isFirstPage = False             # is it the first page of the book ?
        self.backgroundImage = ''           # path + filename of image displayed at background      '' means it will be a string
        self.backgroundMusic = ''           # path + filename of music to be played
        self.backgroundMusicLoops = False   # music must loop ? ie when file finished playing restart it
        self.victory = False                # victorious page ?
        self.death = False                  # death page ?
        # new dictionaries for each pages (they have different monsters, objects ...)
        self.monsters = dict()                # this dictionary will store the possible monsters on a page
        self.objects = dict()                 # this dictionary will store the possible objects on a page
        self.enigms = dict()                  # this dictionary will store the possible enigms on a page
        self.choices = dict()                  # this dictionary will store the possible choices proposed on a page
        return

    def addMonsterToPage(self, aMonster):
        if aMonster.ID not in self.monsters:
            self.monsters[aMonster.ID]=aMonster
        return

    def deleteMonsterOfPage(self, aMonster):
        if aMonster.ID in self.monsters:
            self.monsters.pop(aMonster.ID)
        return

    def addObjectToPage(self, anObject):
        if anObject.ID not in self.objects:
            self.objects[anObject.ID]=anObject
        return

    def deleteObjectOfPage(self, anObject):
        if anObject.ID in self.objects:
            self.objects.pop(anObject.ID)
        return

    def addEnigmToPage(self, anEnigm):
        if anEnigm.ID not in self.enigms:
            self.enigms[anEnigm.ID]=anEnigm
        return

    def deleteEnigmOfPage(self, anEnigm):
        if anEnigm.ID in self.enigms:
            self.enigms.pop(anEnigm.ID)
        return

    def addChoiceToPage(self, aChoice):
        if aChoice.ID not in self.choices:
            self.choices[aChoice.ID]=aChoice
        return

    def deleteChoiceOfPage(self, aChoice):
        if aChoice.ID in self.choices:
            self.choices.pop(aChoice.ID)
        return

    def getDisplayedText(self):
        return self.ID + ' : '+ self.title
