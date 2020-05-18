from Matchup import Matchup
from Player import Player

class PickSummary(object):

    UNDER = -1
    OVER = 1
    EVEN = 0

    def __init__(self, player, matchUp):
        self.player = player
        self.matchUp = matchUp
        self.greenLight = "False"
        self.averageKillsLine = self.EVEN
        self.totalKillsLine = self.EVEN

    def calculateGreenLight(self):
        self.__calculateAverageKillsLine()
        self.__calculateTotalKillsLine()
        if self.averageKillsLine != self.totalKillsLine :
            self.greenLight = "False"
        elif self.averageKills and self.totalKills < 0:
            self.greenLight = "True"
        elif self.averageKills and self.totalKills > 0:
            self.greenLight = "True"
        return self.greenLight


    def __calculateAverageKillsLine(self):
        if self.matchUp.teamOne.averageKills < self.matchUp.teamTwo.averageKills:
            self.averageKillsLine = self.UNDER
        elif self.matchUp.teamOne.averageKills > self.matchUp.teamTwo.averageKills:
            self.averageKillsLine = self.OVER
        else:
            self.averageKills = self.EVEN

    def __calculateTotalKillsLine(self):
        if self.matchUp.teamOne.totalKills < self.matchUp.teamTwo.totalKills:
            self.totalKills = self.UNDER
        elif self.matchUp.teamOne.totalKills > self.matchUp.teamTwo.totalKills:
            self.totalKills = self.OVER
        else:
            self.totalKills = self.EVEN
