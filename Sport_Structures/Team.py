
class Team(object):

    def __init__(self, name, id):
        self.name = name
        self.teamid = id
        self.opponentName = None
        self.opponentID = None
        self.roster = []
        self.averageRoundsPerMatch = 0
        self.prjKills = 0
        self.kdRatio = None
        self.winPercentage = None
        self.mapStats = dict()

    def __str__(self):
        line1 = "Team Name : " + self.name + "\n"
        line2 = "Team ID : " + str(self.teamid) + "\n"
        line3 = "Roster : " + str(self.roster) + "\n"
        line4 = "Average Rounds Per Match : " + str(self.averageRoundsPerMatch) + "\n"
        line5 = "Team Prj Kills : " + str(self.prjKills) + "\n"
        return line1 + line2 + line3 + line4 + line5

    def __repr__(self) :
        return self.name

    def __eq__(self, other):
        return self.name == other
