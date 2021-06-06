import copy
import os
import random
import time
import tkinter as tk
import pygame
import pygame_menu

import HB_Utilities
import Splash
import CurrentGame

# todo JRA try to migrate v1 python player in a class structure !


def launchGamePlayer():

    def itemWasSelected():
        menuContinue.disable()
        pass

    Splash.Splash(None, './images/splashPlayer.gif', 3)
    wantToContinue = True
    mainPlayer = Player()
    while wantToContinue:
        if mainPlayer.SelectBook():
            if mainPlayer.SelectHero():
                mainPlayer.InitGraphicalObjects()
                mainPlayer.PlayBookWithHero()
        # ask to continue playing
        menuContinue = pygame_menu.Menu('Retry ?', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
        menuContinue.add.button('OK', itemWasSelected)
        menuContinue.add.button('Quit', itemWasSelected)
        menuContinue.mainloop(mainPlayer.screen)
        menuContinueAnswer = menuContinue.get_selected_widget().get_title()
        wantToContinue = (menuContinueAnswer == "OK")
        mainPlayer.CleanClose()
        # while continues ?

    pygame.mixer.quit()
    pygame.display.quit()
    pygame.quit()
    return


class Player(object):
    def __init__(self):
        self.theCurrentGame = None
        self.initialPath = os.getcwd()
        self.heroImage = None
        # start of tkinter usage in this module just to get max screen resolution
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()
        # end of tkinter usage in this module

        # Setup for sounds, defaults are good
        pygame.mixer.init()
        # Initialize pygame
        pygame.init()
        # Required to have pygame calculating a correct frame rate
        self.clock = pygame.time.Clock()
        pygame.display.get_surface()

        # Create the screen object
        # if debug we don't want the full screen that prevent to go back to PyCharm
        if __debug__:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

        self.semiTransparentBlack = pygame.image.load('./images/SemiTransparentBlack.png').convert_alpha()

        self.deathOverlay = HB_Utilities.getCenterOfImage('./images/deathOverlay.png', '', (self.screen_width, self.screen_height))
        self.victoryOverlay = HB_Utilities.getCenterOfImage('./images/victoryOverlay.png', '', (self.screen_width, self.screen_height))

        if self.screen_width < 1400:
            self.pageTitleFont = pygame.font.SysFont('arial', 30)
            self.pageCommentFont = pygame.font.SysFont('arial', 20)
            self.heroFont = pygame.font.SysFont('arial', 30)
            self.choiceTitleFont = pygame.font.SysFont('arial', 25)
            self.choiceTitleFontDisabled = pygame.font.SysFont('arial', 20, italic=True)
            self.choiceCommentFont = pygame.font.SysFont('arial', 10)
            self.btnSizeX = self.screen_width / 3
            self.btnSizeY = 48
            self.pageTitleBox = pygame.Rect(150, 20, self.screen_width - 300, 60)
            self.pageCommentBox = pygame.Rect(150, 74, self.screen_width - 300, self.screen_height / 4)
            self.objSizeOnScreen = 384
            self.objInventorySizeOnScreen = 108
            self.objInventoryFont = pygame.font.SysFont('arial', 15)
            self.pageEventFont = pygame.font.SysFont('arial', 40)
        else:
            self.pageTitleFont = pygame.font.SysFont('arial', 50)
            self.pageCommentFont = pygame.font.SysFont('arial', 40)
            self.heroFont = pygame.font.SysFont('arial', 40)
            self.choiceTitleFont = pygame.font.SysFont('arial', 40)
            self.choiceTitleFontDisabled = pygame.font.SysFont('arial', 32, italic=True)
            self.choiceCommentFont = pygame.font.SysFont('arial', 15)
            self.btnSizeX = self.screen_width / 3
            self.btnSizeY = 64
            self.pageTitleBox = pygame.Rect(150, 20, self.screen_width-300, 60)
            self.pageCommentBox = pygame.Rect(150, 98, self.screen_width-300, self.screen_height/5)
            self.objSizeOnScreen = 768
            self.objInventorySizeOnScreen = 128
            self.objInventoryFont = pygame.font.SysFont('arial', 25)
            self.pageEventFont = pygame.font.SysFont('arial', 80)

        self.choiceBoxes = list()
        self.allowed = list()
        for i in range(6):
            theRect = pygame.Rect(
                (i % 3)*self.btnSizeX,
                self.screen_height - 2 * self.btnSizeY - 10 + int(i/3) * self.btnSizeY,
                self.btnSizeX,
                self.btnSizeY).inflate(-5, -5)
            self.choiceBoxes.append(theRect)
            self.allowed.append(False)
        return

    def SelectBook(self):

        ret = False
        # get all folders in 'books' folder make a menu to choose between them
        folder = './books'
        sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

        def itemWasSelected():
            menu.disable()
            pass

        pygame.mixer.music.load(self.initialPath+"/music/MenuChooseBook.mp3")
        pygame.mixer.music.play(loops=-1)

        menu = pygame_menu.Menu('Select a book', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
        for bookName in sub_folders:
            menu.add.button(bookName, itemWasSelected)
        menu.add.button('Quit', itemWasSelected)
        menu.mainloop(self.screen)
        selectedBook = menu.get_selected_widget().get_title()
        if selectedBook == "Quit":
            selectedBook = ""

        pygame.mixer.music.stop()

        if selectedBook != "":
            # we try to load the current book !
            print(selectedBook)
            # change current OS directory to game directory
            newWorkingDirectory = os.path.join("./Books/", selectedBook)
            os.chdir(newWorkingDirectory)
            self.theCurrentGame = CurrentGame.CurrentGame()
            with open('Main.HeroBook', 'rb') as f:
                self.theCurrentGame.book = self.theCurrentGame.book.loadBook('.', f)
                f.close()
                ret = True

        return ret

    def SelectHero(self):
        ret = False

        def itemWasSelected():
            menu.disable()
            pass

        pygame.mixer.music.load(self.initialPath+"/music/MenuChooseHero.mp3")
        pygame.mixer.music.play(loops=-1)

        menu = pygame_menu.Menu('Select a hero', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
        for hero in self.theCurrentGame.book.possibleHeros:
            theHero = self.theCurrentGame.book.possibleHeros[hero]
            menu.add.button(theHero.name, itemWasSelected)
        menu.add.button('Quit', itemWasSelected)
        menu.mainloop(self.screen)
        selectedHeroName = menu.get_selected_widget().get_title()
        if selectedHeroName == "Quit":
            selectedHeroName = ""
        pygame.mixer.music.stop()
        if selectedHeroName != "":
            # as we chose with hero name, we need to find back the hero ID
            chosenHeroID = ''
            for hero in self.theCurrentGame.book.possibleHeros:
                theHero = self.theCurrentGame.book.possibleHeros[hero]
                if theHero.name == selectedHeroName:
                    chosenHeroID = hero
            if chosenHeroID != '':
                # we need to do all the work for this chosen hero within theCurrentGame class instance
                self.theCurrentGame.theCurrentHero.possibleHeroBasedOn =\
                    copy.deepcopy(self.theCurrentGame.book.possibleHeros[chosenHeroID])
                self.theCurrentGame.theCurrentHero.theLiveHero =\
                    copy.deepcopy(self.theCurrentGame.book.possibleHeros[chosenHeroID])
                ret = True
        return ret

    def PlayBookWithHero(self):

        RunGame = True

        currentID = self.theCurrentGame.book.getFirstPageID()
        lastID = ''
        lastReturnPage = ''

        reScaledImage = None

        # we can create the thumbnail of the hero for main screen
        heroImageFilename = self.theCurrentGame.theCurrentHero.theLiveHero.image
        if heroImageFilename != '':
            self.heroImage = HB_Utilities.getSquareCenterOfImage(heroImageFilename, '', 128)

        thePageMusic = ''

        while RunGame:
            thePage = self.theCurrentGame.book.pages[currentID]
            # if ID changed load new image, music ...
            if lastID != currentID:
                # page has changed reload is needed : background image, sound ...
                print("ID ", currentID, lastID)

                # background image
                pageImageFilename = thePage.backgroundImage
                if pageImageFilename != '':
                    reScaledImage = HB_Utilities.getCenterOfImage(pageImageFilename, '', (self.screen_width, self.screen_height))
                else:
                    reScaledImage = None

                lastReturnPage = lastID
                lastID = currentID
                # end of page change

            # display background
            if reScaledImage is not None:
                self.screen.blit(reScaledImage, (0, 0))

            # display Hero values
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 128, 196), width=0, border_radius=0)
            vitalityBarWidth = self.theCurrentGame.theCurrentHero.theLiveHero.lifePoints * 128 / 100
            self.drawText(self.theCurrentGame.theCurrentHero.theLiveHero.name,
                          self.heroFont, 64, 150, (0, 127, 0), (0, 0, 0))
            pygame.draw.rect(self.screen, (0, 255, 0), (0, 170, vitalityBarWidth, 10), width=0, border_radius=3)
            self.drawText(str(int(self.theCurrentGame.theCurrentHero.theLiveHero.lifePoints)),
                          self.choiceCommentFont, 64, 188, (0, 127, 0), (0, 0, 0))

            if self.heroImage is not None:
                self.screen.blit(self.heroImage, (0, 0))

            # display text & comment of current page
            if str(thePage.title) != '':
                if thePage.title[0] == '_': # draw only titles that starts with '_'
                    theTitle = str(thePage.title)
                    theTitle = theTitle[1:]
                    HB_Utilities.drawMultilineText(self.screen, theTitle, self.pageTitleFont, (255, 255, 255),
                                               None, self.semiTransparentBlack, self.pageTitleBox)
            if str(thePage.comment) != '':
                HB_Utilities.drawMultilineText(self.screen, str(thePage.comment), self.pageCommentFont,
                                               (255, 255, 255),
                                               None, self.semiTransparentBlack, self.pageCommentBox)

            x = (self.screen_width - self.objSizeOnScreen) / 2
            y = (self.screen_height - self.objSizeOnScreen) / 2

            # show potential objects
            for o in thePage.objects:
                theObj = thePage.objects[o]
                if theObj.image != '':
                    theImg = HB_Utilities.getSquareThumbnail(theObj.image, '', self.objSizeOnScreen)
                    self.screen.blit(theImg, (x, y))
                    x += 50
                    y += 50

            # show potential enigms
            for e in thePage.enigms:
                theImg = HB_Utilities.getSquareThumbnail(self.initialPath + '/images/enigm.png', '', self.objSizeOnScreen)
                self.screen.blit(theImg, (x, y))
                x += 50
                y += 50

            # show potential monsters
            for m in thePage.monsters:
                theMonster = thePage.monsters[m]
                if theMonster.image != '':
                    theImg = HB_Utilities.getSquareThumbnail(theMonster.image, '', self.objSizeOnScreen)
                    # self.screen.blit(theImg, (x, y))
                    x += 50
                    y += 50

            # show current inventory
            nbInInv = 0
            for i in self.theCurrentGame.theCurrentHero.objectsInventory:
                theObjRectInInventory = pygame.Rect(10, 200 + nbInInv * (self.objInventorySizeOnScreen + 6), self.objInventorySizeOnScreen, self.objInventorySizeOnScreen)
                nbInInv += 1
                theObj = self.theCurrentGame.theCurrentHero.objectsInventory[i]
                HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, theObjRectInInventory)
                if theObj.image != '':
                    theObjRectInInventory.inflate(-6, -6)
                    theObjIm = HB_Utilities.getSquareThumbnail(theObj.image, '', self.objInventorySizeOnScreen)
                    self.screen.blit(theObjIm, theObjRectInInventory.topleft)
                # object text
                theObjRectInInventory.top = theObjRectInInventory.bottom - 20
                HB_Utilities.drawMultilineText(self.screen, theObj.name, self.objInventoryFont, (255, 255, 255), None, None, theObjRectInInventory)

            # Do you take objects ?
            if self.takeAnObject(thePage):
                self.PlaySoundObjectFound()
                thePageMusic = ''
                continue
            # Do you have enigmas to solve ?

            if len(thePage.enigms) > 0:
                if self.solveEnigm(thePage):
                    thePageMusic = ''
                    continue
                else:
                    currentID = lastReturnPage
                    self.PlaySoundOfSteps()
                    thePageMusic = ''
                    continue

            # Do you still have PV to fight ?
            if self.theCurrentGame.theCurrentHero.theLiveHero.lifePoints >= 0:
                # Do you have monsters to fight ?
                if self.fightMonster(self.theCurrentGame.theCurrentHero, thePage):
                    thePageMusic = ''
                    continue

            # music
            if self.theCurrentGame.theCurrentHero.theLiveHero.lifePoints >= 0:
                if thePage.backgroundMusic == '':
                    pygame.mixer.music.stop()
                if thePage.backgroundMusic != '' and thePageMusic != thePage.backgroundMusic:
                    pygame.mixer.music.load(thePage.backgroundMusic)
                    pygame.mixer.music.set_volume(1)
                    if thePage.backgroundMusicLoops:
                        pygame.mixer.music.play(loops=-1)
                    else:
                        pygame.mixer.music.play(loops=0)
                    thePageMusic = thePage.backgroundMusic
            else:
                if thePageMusic != 'death':
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.initialPath+'/music/death.mp3')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
                    thePageMusic = 'death'

            # draw the "menu"
            for i in range(6):
                HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, self.choiceBoxes[i])

            pageChoiceNB = 0
            for i in self.allowed:
                self.allowed[pageChoiceNB] = False
                pageChoiceNB += 1
            pageChoiceNB = 0
            for pageChoice in thePage.choices:
                theChoice = thePage.choices[pageChoice]
                choicePosX = self.choiceBoxes[pageChoiceNB].center[0]
                choicePosY = self.choiceBoxes[pageChoiceNB].center[1]
                # check if the choice is allowed because you have the proper object if yes white font, else gray italic
                if self.currentChoiceIsPossible(theChoice.requiredObjectID):
                    self.drawText(theChoice.shortText, self.choiceTitleFont, choicePosX, choicePosY, (255, 255, 255), None)
                    self.allowed[pageChoiceNB] = True
                else:
                    self.drawText(theChoice.shortText, self.choiceTitleFontDisabled, choicePosX, choicePosY, (96, 96, 96),
                                  None)
                    self.allowed[pageChoiceNB] = False
                pageChoiceNB += 1

            # check if player is dead
            Victory = bool(thePage.victory)
            Death = bool(thePage.death)
            if self.theCurrentGame.theCurrentHero.theLiveHero.lifePoints < 0:
                Death = True

            # check if player loose or win
            if Death:
                HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, pygame.Rect(0, 0, self.screen_width, self.screen_height))
                self.screen.blit(self.deathOverlay, (0, 0))
            elif Victory:
                HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, pygame.Rect(0, 0, self.screen_width, self.screen_height))
                self.screen.blit(self.victoryOverlay, (0, 0))

            choicePosX = self.choiceBoxes[5].center[0]
            choicePosY = self.choiceBoxes[5].center[1]
            self.drawText('Quit', self.choiceTitleFont, choicePosX, choicePosY, (255, 0, 0), None)

            pygame.display.flip()

            # check if events TEST PURPOSE ONLY
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mousePos = pygame.mouse.get_pos()
                    # in bottom button area ?
                    clickedIndex = -1
                    for i in range(6):
                        if self.choiceBoxes[i].left <= mousePos[0] <= self.choiceBoxes[i].right and self.choiceBoxes[i].top <= mousePos[1] <= self.choiceBoxes[i].bottom:
                            clickedIndex = i
                    # if clickedIndex = 5 ==> exit otherwise an action is possible ?
                    theNextPage = ''
                    if clickedIndex < 5:
                        # move only if it is allowed
                        if self.allowed[clickedIndex]:
                            theNextPage = self.GetPageToReachFromClickedIndex(thePage, clickedIndex)
                            if theNextPage != '':
                                currentID = theNextPage
                        else:
                            self.PlaySoundObjectImpossibleChoice()
                            thePageMusic = ''
                    elif clickedIndex == 5:
                        RunGame = False

                    # if not quitting play 1 second of steps and page has changed
                    if clickedIndex != 5 and theNextPage != '':
                        self.PlaySoundOfSteps()
                        thePageMusic = ''

            # display screen
            pygame.display.flip()

        # ensure that no more music is playing
        pygame.mixer.music.stop()
        return

    def currentChoiceIsPossible(self, requiredObjectID):
        ret = True
        if requiredObjectID > '':
            ret = False
            #check if required object is in inventory
            for o in self.theCurrentGame.theCurrentHero.objectsInventory:
                if o == requiredObjectID:
                    ret = True
        return ret

    def PlaySoundOfSteps(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.initialPath + '/music/Pas.mp3')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=0)
        time.sleep(1)
        pygame.mixer.music.stop()
        return

    def PlaySoundObjectFound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.initialPath + '/music/foundObject.mp3')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=0)
        time.sleep(2)
        pygame.mixer.music.stop()
        return

    def PlaySoundObjectImpossibleChoice(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.initialPath + '/music/pain.mp3')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=0)
        time.sleep(1)
        pygame.mixer.music.stop()
        return

    def CleanClose(self):
        os.chdir(self.initialPath)
        return

    def drawText(self, txt, font, x, y, colorFront, colorback):
        text = font.render(txt, True, colorFront, colorback)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)
        return

    def InitGraphicalObjects(self):
        return

    def GetPageToReachFromClickedIndex(self, theCurrentPage, searchedIndex):
        ret = ''
        curIndex = 0
        for pageChoice in theCurrentPage.choices:
            if curIndex == searchedIndex:
                ret = theCurrentPage.choices[pageChoice].reachedPageID
            curIndex += 1
        return ret

    def takeAnObject(self, theCurrentPage):
        ret = False
        if len(theCurrentPage.objects) > 0:
            pygame.display.flip()
            time.sleep(1)

            theObj = None
            for o in theCurrentPage.objects:
                theObj = theCurrentPage.objects[o]
                break
            if theObj is not None:
                # put object in inventory and remove it from page
                self.theCurrentGame.theCurrentHero.objectsInventory[theObj.ID] = theObj
                theCurrentPage.objects.pop(theObj.ID)
                ret = True
        return ret

    def solveEnigm(self, theCurrentPage):
        ret = False

        def itemWasSelected():
            menu.disable()
            pass

        if len(theCurrentPage.enigms) > 0:

            # splash text
            self.drawText("Enigm !", self.pageEventFont, self.screen_width/2, 32, (40, 0, 150), None)
            pygame.display.flip()
            # start suspens music
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.initialPath + '/music/enigmSountrack.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=0)

            time.sleep(2)

            theEnigm = None
            for e in theCurrentPage.enigms:
                theEnigm = theCurrentPage.enigms[e]
                break
            if theEnigm is not None:
                menu = pygame_menu.Menu('Solve Enigm ?', 1000, 700, theme=pygame_menu.themes.THEME_BLUE, center_content=False)
                menu.add.label(HB_Utilities.splitSentence(theEnigm.title, 10))
                menu.add.label(' ')
                menu.add.label(HB_Utilities.splitSentence(theEnigm.comment, 10))
                menu.add.label(' ')
                for t in theEnigm.possibleAnswers:
                    menu.add.button(theEnigm.possibleAnswers[t], itemWasSelected)
                menu.add.button('Quit', itemWasSelected)
                menu.mainloop(self.screen)
                answer = menu.get_selected_widget().get_title()
                foundGoodAnswer = False
                if answer != 'Quit':
                    for a in theEnigm.possibleAnswers:
                        theAnswer = theEnigm.possibleAnswers[a]
                        if theAnswer == answer:
                            if a in theEnigm.goodAnswers:
                                if theEnigm.goodAnswers[a]:
                                    foundGoodAnswer = True

                if answer != 'Quit' and foundGoodAnswer:
                    # enigm solved play victory music
                    theCurrentPage.enigms.pop(theEnigm.ID)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.initialPath + '/music/EnigmVictory.mp3')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=0)
                    time.sleep(3)
                    pygame.mixer.music.stop()
                    ret = True
                else:
                    # play lossmusic
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.initialPath + '/music/EnigmLoss.mp3')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=0)
                    time.sleep(2)
                    pygame.mixer.music.stop()
                    return ret
            return ret

    def fightMonster(self, theCurrentHero, theCurrentPage):
        ret = False
        if len(theCurrentPage.monsters) > 0:
            # splash text
            self.drawText("Fight !", self.pageEventFont, self.screen_width/2, 32, (182, 0, 0), None)
            pygame.display.flip()
            # start suspens music
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.initialPath + '/music/fightSoundtrack.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=0)

            time.sleep(2)

            theMonster = None
            for m in theCurrentPage.monsters:
                theMonster = theCurrentPage.monsters[m]
                break
            if theMonster is not None:
                oneIsDead = False
                theRoundNumber = 0
                arenaImage = HB_Utilities.getCenterOfImage(self.initialPath+'/images/arena.png', '', (self.screen_width, self.screen_height))
                heroImage = HB_Utilities.getSquareThumbnail(theCurrentHero.theLiveHero.image, '', self.screen_height / 2)
                monsterImage = HB_Utilities.getSquareThumbnail(theMonster.image, '', self.screen_height / 2)
                heroAttackImage = HB_Utilities.getSquareThumbnail(self.initialPath+'/images/HeroAttack.png', '', self.screen_width - self.screen_height)
                monsterAttackImage = HB_Utilities.getSquareThumbnail(self.initialPath+'/images/MonsterAttack.png', '', self.screen_width - self.screen_height)
                heroPos = (0, self.screen_height/4)
                monsterPos = (self.screen_width - self.screen_height/2, self.screen_height/4)
                flamePos = ((self.screen_width-heroAttackImage.get_width())/2, (self.screen_height-heroAttackImage.get_height())/2)
                heroBoxMax = pygame.Rect(0, self.screen_height / 4 * 3, self.screen_height / 2, 30)
                monsterBoxMax = pygame.Rect(self.screen_width - self.screen_height / 2, self.screen_height / 4 * 3, self.screen_height / 2, 30)
                while not oneIsDead:
                    # display arena background
                    self.screen.blit(arenaImage, (0, 0))
                    # display persons
                    self.screen.blit(heroImage, heroPos)
                    self.screen.blit(monsterImage, monsterPos)
                    heroBoxLive = pygame.Rect(0, 3+self.screen_height/4*3, self.screen_height/2 * min(100, theCurrentHero.theLiveHero.lifePoints)/100, 24)
                    monsterBoxLive = pygame.Rect(self.screen_width-self.screen_height/2, 3+self.screen_height/4*3, self.screen_height/2 * min(100, theMonster.lifePoints)/100, 24)

                    HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, heroBoxMax)
                    pygame.draw.rect(self.screen, (0, 0, 255), heroBoxLive, 0)
                    self.drawText(str(int(theCurrentHero.theLiveHero.lifePoints)), self.objInventoryFont, heroBoxLive.centerx, heroBoxLive.centery, (255, 255, 255), None)

                    HB_Utilities.drawBoxWithTexture(self.screen, self.semiTransparentBlack, monsterBoxMax)
                    pygame.draw.rect(self.screen, (255, 0, 0), monsterBoxLive, 0)
                    self.drawText(str(int(theMonster.lifePoints)), self.objInventoryFont, monsterBoxLive.centerx, monsterBoxLive.centery, (255, 255, 255), None)

                    # draw attack way
                    if theRoundNumber % 2 == 0:
                        self.screen.blit(heroAttackImage, flamePos)
                    else:
                        self.screen.blit(monsterAttackImage, flamePos)
                    pygame.display.flip()
                    # self.PlayFightSound((theRoundNumber % 2) != 0, 0.1)
                    time.sleep(2)

                    # compute impacts
                    if theRoundNumber % 2 == 0:
                        theMonster.lifePoints -= (int(random.randrange(10)) + 1)
                    else:
                        theCurrentHero.theLiveHero.lifePoints -= (int(random.randrange(10)) + 1)
                    if theMonster.lifePoints < 0 or theCurrentHero.theLiveHero.lifePoints < 0:
                        oneIsDead = True
                    print('Fight in progress     R: ' + str(theRoundNumber) + '     H: ' + str(theCurrentHero.theLiveHero.lifePoints) + '     M: ' + str(theMonster.lifePoints))
                    theRoundNumber += 1
                # if monster is dead nice sound and remove it from page and ret becomes true
                if theMonster.lifePoints < 0:
                    self.drawText("Win !", self.pageEventFont, self.screen_width / 2, self.screen_height / 2,
                                  (0, 255, 255), None)
                    pygame.display.flip()
                    self.PlayFightSound(True, 1.0)
                    time.sleep(3)
                    theCurrentPage.monsters.pop(theMonster.ID)
                    ret = True
                # if player is dead bad sound
                if theCurrentHero.theLiveHero.lifePoints < 0:
                    self.drawText("Lost !", self.pageEventFont, self.screen_width / 2, self.screen_height / 2,
                                  (255, 0, 0), None)
                    pygame.display.flip()
                    self.PlayFightSound(False, 1.0)
                    time.sleep(3)
            return ret


    def PlayFightSound(self, goodSound, theVolume):
        pygame.mixer.music.stop()
        if goodSound:
            pygame.mixer.music.load(self.initialPath + '/music/EnigmVictory.mp3')
        else:
            pygame.mixer.music.load(self.initialPath + '/music/EnigmLoss.mp3')
        pygame.mixer.music.set_volume(theVolume)
        pygame.mixer.music.play(loops=0)
        return
