
class Team(object):

    def __init__(self, name, id):
        self.name = name
        self.teamid = id
        self.roster = []
        self.averageKills = 0
        self.totalKills = 0

    def calculateKillStats(self):
        totalKills = 0
        for player in self.roster:
            totalKills += player.prjKillsWithOvertime
        self.averageKills = totalKills/len(self.roster)
        self.totalKills = totalKills
