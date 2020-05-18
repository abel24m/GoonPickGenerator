
from Team import Team

class Matchup(object):

    def __init__(self, teamOne, teamTwo):
        self.teamOne = teamOne
        self.teamTwo = teamTwo

    def __repr__(self):
        lineOne = "--------MatchUp--------\n"
        lineTwo = "Team one name : " + self.teamOne.name + "\n"
        lineThree = "Team one id : " + str(self.teamOne.teamid) + "\n"
        lineFour = "Team two name : " + self.teamTwo.name + "\n"
        lineFive = "Team two id : " + str(self.teamTwo.teamid) + "\n"
        return lineOne+lineTwo+lineThree+lineFour+lineFive
