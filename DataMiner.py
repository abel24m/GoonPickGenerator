
import requests
import time
from Team import Team
from Player import Player
from Matchup import Matchup

class DataMiner(object):

    url = "https://whispering-bayou-49673.herokuapp.com/"
    MAPS_MINIMUM = 0
    NUMBER_OF_MATCHES = 8
    OVERTIME_SCORE = 16
    MAX_NUM_OF_RETRIES = 5


    def __init__(self, MAPS_MINIMUM):
        super(DataMiner, self).__init__()
        self.MAPS_MINIMUM = int(MAPS_MINIMUM)

    def doesPlayerExist(self,name):
        params = {"name" : name}
        response = requests.get(self.url + "player", params = params)
        status = response.status_code
        if str(status).startswith('5'):
            print("Player named " + name + "does not exist")
            return False
        else :
            return True

    def getPlayerKpr(self,name):
        params = {"name" : name}
        numOfTries = 0
        while numOfTries < self.MAX_NUM_OF_RETRIES :
            try :
                playerData = requests.get(self.url + "player", params = params).json()
                break
            except :
                numOfTries += 1
                print("Error trying to ket KPR.........trying again")
        kpr = playerData["statistics"]["killsPerRound"]
        return kpr

    def getAverageRoundsPerSeries(self, name, withOvertime):
        print("-------- " + name + " -----------")
        teamID = self.__getPlayerTeamID(name)
        params = {"teamid" : teamID}
        teamData = requests.get(self.url + "team", params = params).json()
        count = 0
        totalRounds = 0
        getcalls = 0
        for match in teamData["recentResults"]:
            time.sleep(1)
            if match["result"] != "-:-":
                matchId = match["matchID"]
                getcalls += 1
                if withOvertime :
                    matchTotal = self.__getMatchTotalsWithOvertime(matchId)
                else :
                    matchTotal = self.__getMatchTotals(matchId)
                if matchTotal != 0:
                    count += 1
                    totalRounds += matchTotal
            if count >= self.NUMBER_OF_MATCHES :
                break
        average = totalRounds/count
        return average



    def evaluateMatchup(self, playerName):
        teamID = self.__getPlayerTeamID(playerName)
        teamName = self.__getPlayerTeamName(playerName)
        oppTeamID = self.__getOppTeamID(playerName)
        oppTeamName = self.__getOppTeamName(playerName)
        team = Team(teamName, teamID)
        oppTeam = Team(oppTeamName, oppTeamID)
        self.__getTeam(team)
        self.__getTeam(oppTeam)
        team.calculateKillStats()
        oppTeam.calculateKillStats()
        playerMatchUp = Matchup(team, oppTeam)
        return playerMatchUp

    def __getTeam(self, team):
        params = {"teamid" : team.teamid}
        teamData = requests.get(self.url + "team", params = params).json()
        count = 0
        for player in teamData["players"]:
            print(count)
            if count >= 5 :
                break
            if self.doesPlayerExist(player["name"]):
                newPlayer = Player(player["name"], -1)
                newPlayer.kpr = self.getPlayerKpr(newPlayer.name)
                newPlayer.avgRounds = self.getAverageRoundsPerSeries(newPlayer.name, False)
                newPlayer.prjKills = newPlayer.kpr*newPlayer.avgRounds
                newPlayer.avgRoundsWithOvertime = self.getAverageRoundsPerSeries(newPlayer.name, True)
                newPlayer.prjKillsWithOvertime = newPlayer.kpr * newPlayer.avgRoundsWithOvertime
                team.roster.append(newPlayer)
                count += 1

    def __getOppTeamName(self,playerName):
        playerTeamID = self.__getPlayerTeamID(playerName)
        params = {"teamid" : playerTeamID}
        teamData = requests.get(self.url + "team", params = params).json()
        oppTeamName = teamData["recentResults"][0]["enemyTeam"]["name"]
        return oppTeamName

    def __getOppTeamID(self,playerName):
        playerTeamID = self.__getPlayerTeamID(playerName)
        params = {"teamid" : playerTeamID}
        teamData = requests.get(self.url + "team", params = params).json()
        oppTeamID = teamData["recentResults"][0]["enemyTeam"]["id"]
        return oppTeamID

    def __getPlayerTeamName(self, playerName):
        params = {"name" : playerName}
        playerData = requests.get(self.url + "player", params = params).json()
        teamName = playerData["team"]["name"]
        return teamName


    def __getPlayerTeamID(self,name):
        params = {"name" : name}
        playerData = requests.get(self.url + "player", params = params).json()
        teamName = playerData["team"]["name"]
        teamID = playerData["team"]["id"]
        return teamID

    def __getMatchTotals(self, matchID):
        params = {"matchid" : matchID}
        try:
            matchData = requests.get(self.url + "match", params = params).json()
        except:
            print("I got stuck. Trying Again")
            self.__getMatchTotals(matchID)
        matchTotal = 0
        totalRounds = 0
        if len(matchData["maps"]) >= self.MAPS_MINIMUM :
            count = 0
            for map in matchData["maps"]:
                if "result" in map:
                    parsedResults = map["result"].split()
                    roundsParsed = parsedResults[0].split(':')
                    if "-" not in roundsParsed:
                        count += 1
                        for rounds in roundsParsed :
                            if int(rounds) <= self.OVERTIME_SCORE :
                                totalRounds += int(rounds)
                            else :
                                return 0
                if count >= self.MAPS_MINIMUM :
                    break;
        return totalRounds

    def __getMatchTotalsWithOvertime(self, matchID):
        params = {"matchid" : matchID}
        matchData = requests.get(self.url + "match", params = params).json()
        matchTotal = 0
        totalRounds = 0
        if len(matchData["maps"]) >= self.MAPS_MINIMUM :
            count = 0
            for map in matchData["maps"] :
                if "result" in map:
                    parsedResults = map["result"].split()
                    roundsParsed = parsedResults[0].split(':')
                    if "-" not in roundsParsed:
                        count += 1
                        for rounds in roundsParsed :
                                totalRounds += int(rounds)
                if count >= self.MAPS_MINIMUM:
                    break;
        return totalRounds
