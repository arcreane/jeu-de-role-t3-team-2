import datetime as dt

class Monster:

    def __init__(self):
        self.ID = '_M'+dt.datetime.now().strftime("%Y%m%d %H%M%S")   # unique ID that identifies the monster
        self.author = ''                  # free string entered by the author in design mode
        self.creationDate = dt.datetime.now().strftime("%Y%m%d %H%M%S") # monster creation date
        self.name = 'New Monster'                    # name of the monster
        self.description = ''             # short description
        self.race = ''                    # short description of the race
        self.origin = ''                  # short description of the origin
        self.image = ''                   # path + filename of image that will be showed to the player
        self.height = 1.0                 # height in meter
        self.lifePoints = 0.0              # monster vitality attributes life points (LP)
        self.strength = 0.0                # max possible LP could be removed to others
        self.resistance = 0.0              # min attack strength to start remove LP when attacked by player
        self.agility = 0.0              # min attack strength to start remove LP when attacked by player
        self.recovery = 0.0              # min attack strength to start remove LP when attacked by player
        return
