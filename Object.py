import datetime as dt

class Object:

    def __init__(self):
        self.ID = '_O'+dt.datetime.now().strftime("%Y%m%d %H%M%S")   # unique ID that identifies the object
        self.author = ''                  # free string entered by the author in design mode
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S")            # object creation date
        self.name = 'New Object'                    # name of the object
        self.comment = ''                 # short description of the object
        self.image = ''                   # path + filename of image that will be showed to the player
        return
