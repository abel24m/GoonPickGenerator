
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
    sheet = client.open('CS:GO Prize Picks').worksheet("Tali")

    def __init__(self):
        self.sheet.clear()
        titles = ["Player", "PrizePick", "Projected Kills", "Spread", "Prj Kills w/Overtime", "Spd w/Overtime", "totalSpreadCombined"]
        count = 1
        for title in titles:
            self.sheet.update_cell(1, count, title)
            count += 1

    def populateExcel(self, playerData):
        iterator = 1
        for data in playerData:
            self.sheet.update_cell(self.rowNumber, iterator, data)
            iterator += 1
        self.rowNumber += 1
        pass
