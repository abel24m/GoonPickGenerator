
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ExcelWriter(object):

    rowNumber = 2

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open('CS:GO Prize Picks').worksheet("TestSheet")

    def __init__(self):
        self.rowNumber = 2
        self.sheet.clear()

    def csgo_output_Results(self, csgo_metaData):
        self.__print_CSGO_Players(csgo_metaData)
        self.rowNumber += 4
        self.__print_CSGO_Teams(csgo_metaData)

    def __print_CSGO_Players(self, csgo_metaData) :
        titles = ["Player", "PrizePick", "Projected Kills", "Spread", "Under/Over"]
        count = 1
        for title in titles:
            self.sheet.update_cell(1, count, title)
            count += 1
        iterator = 1
        for player in csgo_metaData["players"]:
            self.sheet.update_cell(self.rowNumber, iterator, player.name)
            self.sheet.update_cell(self.rowNumber, iterator + 1, player.prizepick)
            self.sheet.update_cell(self.rowNumber, iterator + 2, player.prjKills)
            self.sheet.update_cell(self.rowNumber, iterator + 3, player.spread)
            self.sheet.update_cell(self.rowNumber, iterator + 4, player.und_ov)
            self.sheet.update_cell(self.rowNumber, iterator + 5, player.team)
            self.rowNumber += 1

    def __print_CSGO_Teams(self, csgo_metaData) :
        titles = ["Team", "Projected Team Kills"]
        count = 1
        for title in titles:
            self.sheet.update_cell(self.rowNumber-1, count, title)
            count += 1
        iterator = 1
        for key, teamDict in csgo_metaData["matchups"].items():
            team = teamDict["team"]
            opponent = teamDict["opponent"]
            self.sheet.update_cell(self.rowNumber, iterator, team.name)
            self.sheet.update_cell(self.rowNumber, iterator + 1, team.prjKills)
            self.sheet.update_cell(self.rowNumber, iterator + 2, opponent.name)
            self.sheet.update_cell(self.rowNumber, iterator + 3, opponent.prjKills)
            self.rowNumber += 1
