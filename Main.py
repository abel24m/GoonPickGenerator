import requests
import json
from Player import Player
from DataMiner import DataMiner
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open('CS:GO Prize Picks').get_worksheet(1)

titles = ["Player", "PrizePick", "Projected Kills", "Spread", "Prj Kills w/Overtime", "Spd w/Overtime"]

count = 1
for title in titles:
    sheet.update_cell(1, count, title)
    count += 1

testmode = 0

players = []
response = "y"
correct = "n"
if not testmode:
    while response == "y" :
        while correct == "n":
            name = input("Please enter a name : ")
            correct = input("Is " + name + " correct? [y/n]")
        prizepick = input("Please enter the PrizePick projection : ")
        player = Player(name, prizepick)
        players.append(player)
        response = input("Do you want to add another player? [y/n] : ")
        correct = "n"
else :
    player = Player("Jame", 41.5)
    players.append(player)

dataMiner = DataMiner()
num = 2
for player in players:
    player.kpr = dataMiner.getPlayerKpr(player.name)
    player.avgRounds = dataMiner.getAverageRoundsPerSeries(player.name, False)
    player.prjKills = player.kpr*player.avgRounds
    player.avgRoundsWithOvertime = dataMiner.getAverageRoundsPerSeries(player.name, True)
    player.prjKillsWithOvertime = player.kpr*player.avgRoundsWithOvertime
    spread = player.prjKills - float(player.prizepick)
    spreadWithOvertime = player.prjKillsWithOvertime - float(player.prizepick)
    playerData = [player.name, player. prizepick, player.prjKills, spread, player.prjKillsWithOvertime, spreadWithOvertime]
    iterator = 1
    for data in playerData:
        sheet.update_cell(num, iterator, data)
        iterator += 1
    num += 1
