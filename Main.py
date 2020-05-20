import requests
import json
import threading
from Player import Player
from DataMiner import DataMiner
from ExcelWriter import ExcelWriter
from Matchup import Matchup
from PickSummary import PickSummary




testmode = 0    #To run the code in test mode 1=testmode 0=not in testmode
players = []    #List of players that are in prizepicks and we will be building projections for

response = "y"
correct = "n"
playerExist = True
if not testmode:
    rowStart = input("What row do you wish to start writing in the excel : ")
    numOfMaps = input("How many maps do you want to use for projections 1 or 2: ")
    while response == "y" :
        name = input("Please enter a name : ")
        prizepick = input("Please enter the PrizePick projection : ")
        player = Player(name, prizepick)
        players.append(player)
        while True:
            response = input("Do you want to add another player? [y/n] : ")
            if response == 'y' or response == 'n':
                break
            else:
                print("Please enter 'y' or 'n'.")
        correct = "n"
else :
    player = Player("Jame", 41.5)
    players.append(player)
    numOfMaps = 2


ExcelWriter = ExcelWriter(rowStart)
dataMiner = DataMiner(numOfMaps)
for player in players:
    if dataMiner.doesPlayerExist(player.name):
        print("Starting Data Mine on " + player.name)
        playerMatchUp = dataMiner.evaluateMatchup(player.name)
        player.kpr = dataMiner.getPlayerKpr(player.name)
        player.avgRounds = dataMiner.getAverageRoundsPerSeries(player.name, False)
        player.prjKills = player.kpr*player.avgRounds
        player.avgRoundsWithOvertime = dataMiner.getAverageRoundsPerSeries(player.name, True)
        player.prjKillsWithOvertime = player.kpr*player.avgRoundsWithOvertime
        player.spread = player.prjKills - float(player.prizepick)
        player.spreadWithOvertime = player.prjKillsWithOvertime - float(player.prizepick)
        totalCombinedSpread = abs(player.spread + player.spreadWithOvertime)
        pickSummary = PickSummary(player, playerMatchUp)
        pickSummary.calculateGreenLight()
        playerData = [player.name, player. prizepick, player.prjKills, player.spread, player.prjKillsWithOvertime,
                    player.spreadWithOvertime, totalCombinedSpread, playerMatchUp.teamOne.averageKills,
                    playerMatchUp.teamOne.totalKills, playerMatchUp.teamTwo.averageKills, playerMatchUp.teamTwo.totalKills, pickSummary.greenLight]
        ExcelWriter.populateExcel(playerData)
