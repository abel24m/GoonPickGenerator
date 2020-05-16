
class Player(object):

    def __init__(self, name, prizepick):
        self.name = name
        self.kpr = 0
        self.avgRounds = 0
        self.prizepick = prizepick
        self.prjKills = 0
        self.avgRoundsWithOvertime = 0
        self.prjKillsWithOvertime = 0
        self.percentageOfConfidence = 0.0
        self.totalSpreadCombined = 0
        self.spread = 0
        self.spreadWithOvertime = 0
