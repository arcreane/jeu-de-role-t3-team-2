import os
import shutil
import tkinter as tk
from tkinter import messagebox  # idem for Yes/No/Cancel messageboxes
import pygame


def CenterTK(theTk):
    if theTk is not None:
        # first update is required to ensure we know width and height of the window
        theTk.update()

        windowWidth = theTk.winfo_reqwidth()
        windowHeight = theTk.winfo_reqheight()
        print("Width", windowWidth, "Height", windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(theTk.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(theTk.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        geometryString = "+{}+{}".format(positionRight, positionDown)
        theTk.geometry(geometryString)

        ## required to make window show before the program gets to the mainloop
        theTk.update()

    return


def RemoveTKBorders(theTK):
    # trick to remove border of a window
    theTK.overrideredirect(1)
    return


def AreYouSure(parent, title, message):
    ret = False
    mbRet = tk.messagebox.askokcancel(
        title=title,
        message=message,
        default=tk.messagebox.CANCEL,
        parent=parent)
    if mbRet:
        ret=True
    return ret


def OKMBox(parentWindow, title, message):
    return tk.messagebox.showinfo(parent=parentWindow, title=title, message=message)


def EraseFolderData(folder):
    ret = True
    localFolder = folder.replace('\\', '/')
    for filename in os.listdir(localFolder):
        file_path = os.path.join(localFolder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            ret = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return ret


def drawMultilineText(surface, text, selectedFont, selectedColor, selectedBackColor, selectedBackground, targetRect):
    h = calculateHeightOfMultilineText(surface, text, selectedFont, selectedColor, selectedBackColor, targetRect)
    if selectedBackColor is not None:
        theRect = pygame.Rect(targetRect.left, targetRect.top, targetRect.width, h)
        pygame.draw.rect(surface, selectedBackColor, theRect, 0)
    if selectedBackground is not None:
        h = calculateHeightOfMultilineText(surface, text, selectedFont, selectedColor, selectedBackColor, targetRect)
        newImage = pygame.transform.scale(selectedBackground, (targetRect.width+20, h+20))
        surface.blit(newImage, (targetRect.left-10, targetRect.top-10))
    if ' ' in text:
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = selectedFont.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x = targetRect.left
        y = targetRect.top
        for line in words:
            for word in line:
                word_surface = selectedFont.render(word , 0, selectedColor)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= targetRect.right:
                    x = targetRect.left  # Reset the x.
                    y += word_height  # Start on new row.
                if y < targetRect.bottom - word_height:
                    surface.blit(word_surface, (x, y))
                x += word_width + space
            x = targetRect.left  # Reset the x.
            y += word_height  # Start on new row.
    else:
        word_surface = selectedFont.render(text, 0, selectedColor)
        surface.blit(word_surface, (targetRect[0], targetRect[1]))
    return


def drawBoxWithTexture(surface, selectedBackground, targetRect):
    if selectedBackground is not None:
        newImage = pygame.transform.scale(selectedBackground, (targetRect.width, targetRect.height))
        surface.blit(newImage, (targetRect.left, targetRect.top))

def calculateHeightOfMultilineText(surface, text, selectedFont, selectedColor, selectedBackColor, targetRect):
    retValue = 0
    if ' ' in text:
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = selectedFont.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x = targetRect.left
        y = targetRect.top
        for line in words:
            for word in line:
                word_surface = selectedFont.render(word , 0, selectedColor, selectedBackColor)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= targetRect.right:
                    x = targetRect.left  # Reset the x.
                    y += word_height  # Start on new row.
                x += word_width + space
            x = targetRect.left  # Reset the x.
            y += word_height  # Start on new row.
        if x!= targetRect.left:
            retValue = y + word_height
        else:
            retValue = y
    else:
        word_surface = selectedFont.render(text, 0, selectedColor, selectedBackColor)
        retValue = targetRect.top + word_surface.get_size()[1]

    return retValue-targetRect.top

def splitSentence(text, maxWordsPerLine):
    retValue = ''

    if ' ' in text:
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        wordNb = 0
        for l in words:
            for w in l:
                retValue += w + ' '
                wordNb +=1
                if wordNb % maxWordsPerLine == 0:
                    retValue += '\n'
    else:
        retValue = text

    return retValue



def getSquareCenterOfImage(sourceFilename, targetFilename, squareSize):
    return getCenterOfImage(sourceFilename, targetFilename, (squareSize, squareSize))


def getCenterOfImage(sourceFilename, targetFilename, targetSize):
    loadedImage = pygame.image.load(sourceFilename).convert_alpha()
    w, h = loadedImage.get_size()
    if w/h > targetSize[0]/targetSize[1]:
        newW = h/targetSize[1]*targetSize[0]
        srcRect = pygame.Rect((w-newW)/2, 0, newW, h)
    else:
        newH = w/targetSize[0]*targetSize[1]
        srcRect = pygame.Rect(0, (h-newH)/2, w, newH)
    newImage = loadedImage.subsurface(srcRect)
    newImage = pygame.transform.scale(newImage, (targetSize[0], targetSize[1]))
    if targetFilename != '':
        pygame.image.save(newImage, targetFilename)
    return newImage

def getSquareThumbnail(sourceFilename, targetFilename, squareSize):
    loadedImage = pygame.image.load(sourceFilename).convert_alpha()
    w, h = loadedImage.get_size()
    if w>h:
        srcRect = pygame.Rect((w-h)/2, 0, h, h)
    else:
        srcRect = pygame.Rect(0, (h-w)/2, w, w)
    newImage = loadedImage.subsurface(srcRect)
    squareSize = int(squareSize)
    newImage = pygame.transform.scale(newImage, (squareSize, squareSize))
    if targetFilename != '':
        pygame.image.save(newImage, targetFilename)
    return newImage

