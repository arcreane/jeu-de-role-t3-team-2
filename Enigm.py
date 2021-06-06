import datetime as dt


class Enigm:

    def __init__(self):
        self.ID = '_E'+dt.datetime.now().strftime("%Y%m%d %H%M%S")  # unique ID that identifies the page
        self.author = ''                  # free string entered by the author in design mode
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S")            # page creation date
        self.title = 'New Enigm'          # title of the page
        self.comment = ''                 # text written at top
        self.possibleAnswers = dict()     # this dictionary to store all possible answers to the enigm
        self.goodAnswers = dict()       # this dictionary to store if answer is good (True) or not (False)
        return

    def addPossibleAnswerToEnigm(self, answerID, answerText, isGoodAnswerYN):
        # add possible answer to an enigm ,
        # text of possible answer is 'answerText',
        # if it is a good answer 'isGoodAnswerYN' is True
        if answerID not in self.possibleAnswers:
            self.possibleAnswers[answerID]=answerText
        if answerID in self.goodAnswersID:
            self.goodAnswersID.pop(answerID)
            if isGoodAnswerYN:
                self.goodAnswersID[answerID]=True
        return

    def deletePossibleAnswerOfEnigm(self, answerID):
        if answerID in self.possibleAnswers:
            self.possibleAnswers.pop(answerID)
        if answerID in self.goodAnswersID:
            self.goodAnswersID.pop(answerID)
        return


