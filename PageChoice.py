import datetime as dt

class PageChoice:

    def __init__(self):
        self.ID = 'PC'+dt.datetime.now().strftime("%Y%m%d %H%M%S")                       # unique ID that identifies the page
        self.shortText = 'New Page Choice' # free string entered by the author in design mode
        self.longText = ''                 # text written at top
        self.reachedPageID = ''            # ID of the page of the book that will be reached if this choice is selected
        self.requiredObjectID = ''         # ID of a required object if needed to select the choice otherwise ''
        return

