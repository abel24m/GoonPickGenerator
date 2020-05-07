import requests
import json
from Player import Player
from DataMiner import DataMiner
from ExcelWriter import ExcelWriter


testmode = 0
players = []

response = "y"
correct = "n"
playerExist = True
if not testmode:
    numOfMaps = input("How many maps do you want to use for projections 1 or 2: ")
    while response == "y" :
        while correct == "n" and playerExist:
            name = input("Please enter a name : ")
            correct = input("Is " + name + " correct? [y/n]")
        prizepick = input("Please enter the PrizePick projection : ")
        player = Player(name, prizepick)
        players.append(player)
        response = input("Do you want to add another player? [y/n] : ")
        correct = "n"
else :
    player = Player("Jame", 41.5)
    self.players.append(player)


ExcelWriter = ExcelWriter()
dataMiner = DataMiner(numOfMaps)
for player in players:
    if dataMiner.doesPlayerExist(player.name):
        print("Starting Data Mine on " + player.name)
        player.kpr = dataMiner.getPlayerKpr(player.name)
        player.avgRounds = dataMiner.getAverageRoundsPerSeries(player.name, False)
        player.prjKills = player.kpr*player.avgRounds
        player.avgRoundsWithOvertime = dataMiner.getAverageRoundsPerSeries(player.name, True)
        player.prjKillsWithOvertime = player.kpr*player.avgRoundsWithOvertime
        spread = player.prjKills - float(player.prizepick)
        spreadWithOvertime = player.prjKillsWithOvertime - float(player.prizepick)
        playerData = [player.name, player. prizepick, player.prjKills, spread, player.prjKillsWithOvertime, spreadWithOvertime]
        ExcelWriter.populateExcel(playerData)
