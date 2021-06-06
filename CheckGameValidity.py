import Book


def checkValidity(currentBook):
    returnString = ""

    # check if book has page and heroes
    if len(currentBook.pages) < 1:
        returnString = returnString + "The book has no pages ! \n"
    if len(currentBook.possibleHeros) < 1:
        returnString = returnString + "The book has no possible Heroes to choose from ! \n"

    if currentBook.getFirstPageID() == "":
        returnString = returnString + "The book has no starting page ! \n"

    for page in currentBook.pages:
        thePage=currentBook.pages[page]
        if len(thePage.choices) < 1:
            returnString = returnString + "The page '" + thePage.ID + "' has no choice page ! \n"
        else:
            for choice in thePage.choices:
                theChoice = thePage.choices[choice]
                if theChoice.reachedPageID == "":
                    returnString = returnString + "The page choice  '" + theChoice.ID + "' has no target page ! \n"

    for hero in currentBook.possibleHeros:
        theHero = currentBook.possibleHeros[hero]
        if theHero.name == '':
            returnString = returnString + "The hero  '" + theHero.ID + "' has no name ! \n"
        if theHero.image == '':
            returnString = returnString + "The hero  '" + theHero.ID + "' has no image file ! \n"

    return returnString