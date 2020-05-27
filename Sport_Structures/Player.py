
class Player(object):

    def __init__(self, name, prizepick, numOfMaps):
        self.name = name
        self.playerid = 0
        self.team = ""
        self.teamid = 0
        self.kpr = 0
        self.prizepick = prizepick
        self.prjKills = 0
        self.spread = 0
        self.numOfMaps = numOfMaps
        self.und_ov = None

    def __str__(self):
        line1 = "\nName : " + self.name + "\n"
        line2 = "Team : " + self.team + "\n"
        line3 = "TeamID : " + str(self.teamid) + "\n"
        line4 = "KPR : " + str(self.kpr) + "\n"
        line5 = "Spread : " + str(self.spread) + "\n"
        line6 = "prjKills : " + str(self.prjKills) + "\n"
        return line1 + line2 + line3 + line4 + line5 + line6

    def __repr__(self) :
        return self.name
