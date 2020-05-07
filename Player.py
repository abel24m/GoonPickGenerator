
class Player(object):

    def __init__(self, name, prizepick):
        self.name = name
        self.kpr = 0
        self.avgRounds = 0
        self.prizepick = prizepick
        self.prjKills = 0
        self.avgRoundsWithOvertime = 0
        self.prjKillsWithOvertime = 0
