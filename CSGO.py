
from Input_Output.IO_Manager import IO_Manager
from Gadgets.DataMiner import DataMiner
from Sport_Structures.Team import Team
from Input_Output.ExcelWriter import ExcelWriter

class CSGO(object):

    def __init__(self):
        self.io_manager = IO_Manager()
        self.metaData = dict()
        # Definition of MetaData and what it entails
        # MetaData:
        #     ["rowStart"] = Number of which row to start writing in the excel document
        #     ["numOfMaps"] = The number of Maps the calculation needs to be done with per players
        #     ["players"] = A list of player objects that will be proccessed and produced a projection
        #     ["matchups"] = Dictionary that has every Team we are developing picks for. Keys are Team Names= Values are
        #                Team Objects
        self.dataMiner = DataMiner()
        self.excelWriter = ExcelWriter()
        pass

    def start(self):
        self.io_manager.init_CSGO(self.metaData)
        self.io_manager.request_CSGO_MetaData(self.metaData)

    def retrieve_Data(self):
        teams = dict()
        for player in self.metaData["players"] :
            if self.dataMiner.getPlayerData(player) :
                if player.team not in teams :
                    teamDict = dict()
                    newTeam = Team(player.team, player.teamid)
                    self.dataMiner.getTeamData(newTeam)
                    teamDict["team"] = newTeam
                    teams[newTeam.name] = teamDict
        self.metaData["matchups"] = teams

    def process_Data(self):
        self.__process_PlayerData()
        self.__process_TeamData()

    def caculate_results(self):
        pass
        #calculateWinStats



    def output_Results(self) :
        self.excelWriter.csgo_output_Results(self.metaData)

    def __process_PlayerData(self):
        for player in self.metaData["players"] :
            team = self.metaData["matchups"].get(player.team)["team"] #this is a complicated line might want to simplify
            player.prjKills = (float(player.kpr) * team.averageRoundsPerMatch) * player.numOfMaps
            player.spread = player.prjKills - player.prizepick
            if player.spread < 0 :
                player.und_ov = "UNDER"
            else :
                player.und_ov = "OVER"
            player.spread = abs(player.spread)

    def __process_TeamData(self):
        for teamDict in self.metaData["matchups"].values() :
            team = teamDict["team"]
            self.__calculate_TeamProjectedKills(team)
            #add the opponent to the team matchups get opponent data if not in data
            opponentName = team.opponentName
            opponentDict = self.metaData["matchups"].get(opponentName)
            if not opponentDict:
                print("No opponent")
                opponent = Team(team.opponentName, team.opponentID)
                opponentDict = dict()
                self.dataMiner.getTeamData(opponent)
                self.__calculate_TeamProjectedKills(opponent)
                opponentDict["team"] = opponent
                opponentDict["opponent"] = team
            teamDict["opponent"] = opponentDict["team"]

    def __calculate_TeamProjectedKills(self,team):
        prjTeamKills = 0
        for player in team.roster :
            player.prjKills = (float(player.kpr) * team.averageRoundsPerMatch) * 2
            prjTeamKills += player.prjKills
        team.prjKills = prjTeamKills
