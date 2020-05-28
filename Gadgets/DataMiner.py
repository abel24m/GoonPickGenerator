
import requests
import time
from Sport_Structures.Team import Team
from Sport_Structures.Player import Player
from Matchup import Matchup

class DataMiner(object):

    url = "https://whispering-bayou-49673.herokuapp.com/"
    MAPS_MINIMUM = 0
    NUMBER_OF_MATCHES = 8
    OVERTIME_SCORE = 16
    MAX_NUM_OF_RETRIES = 3


    def __init__(self):
        pass

    def getPlayerData(self,player):
        self.__getPlayerID(player)
        params = {"playerid" : player.playerid}
        numOfTries = 0
        while numOfTries is not self.MAX_NUM_OF_RETRIES :
            response = requests.get(self.url + "playerstats", params = params)
            if response.status_code is 200:
                playerData = response.json()
                break
            else :
                print ("Error Getting Player Data")
                print (self.url + "playerstats?playerid=" + str(player.playerid))
                print (response)
                time.sleep(3)
                print("Trying Again...")
                numOfTries += 1
        if numOfTries is self.MAX_NUM_OF_RETRIES:
            return 0
        player.kpr = playerData["statistics"]["killsPerRound"]
        player.team = playerData["team"]["name"]
        player.teamid = playerData["team"]["id"]
        return 1


    def getTeamData(self,team):
        self.__getTeamOpponent(team)
        params = {"teamid" : team.teamid}
        numOfTries = 0
        while numOfTries is not self.MAX_NUM_OF_RETRIES :
            response = requests.get(self.url + "teamstats", params = params)
            if response.status_code is 200:
                teamData = response.json()
                break
            else:
                print("Error Getting Team Data")
                print (self.url + "teamstats?teamid=" + team.teamid)
                print (response)
                time.sleep(3)
                print("Trying Again...\n")
                numOfTries += 1
        if numOfTries is self.MAX_NUM_OF_RETRIES:
            return 0
        #Grab Roster
        for player in teamData["currentLineup"]:
                newPlayer = Player(player["name"], -1, 0)
                self.getPlayerData(newPlayer)
                team.roster.append(newPlayer)
        #Grab and Calculate Average Rounds per Match
        numOfMatches = 0
        totalRounds = 0
        for match in teamData["matches"] :
            result = match["result"]
            result = result.split()
            totalRounds += int(result[0]) + int(result[2])
            numOfMatches += 1
            if numOfMatches >= 25 :
                break
        team.averageRoundsPerMatch = totalRounds/float(numOfMatches)
        #Get Team Overview Stats
        team.kdRatio = teamData["overview"]["kdRatio"]
        wins = teamData["overview"]["wins"]
        losses = teamData["overview"]["losses"]
        team.winPercentage = float(wins)/(wins+losses)
        #Get Map Stats
        for map, stats in teamData["mapStats"].items() :
            team.mapStats[map] = stats
        return 1

    def __getTeamOpponent(self, team):
        params = {"teamid" : team.teamid}
        numOfTries = 0
        while numOfTries is not self.MAX_NUM_OF_RETRIES :
            response = requests.get(self.url + "team", params = params)
            if response.status_code is 200:
                teamData = response.json()
                break
            else:
                print("Error Getting Team Data")
                print (self.url + "team?teamid=" + team.teamid)
                print (response)
                time.sleep(3)
                print("Trying Again...\n")
                numOfTries += 1
        if numOfTries is self.MAX_NUM_OF_RETRIES:
            return 0
        #Populate Opponent Data
        team.opponentName = teamData["recentResults"][0]["enemyTeam"]["name"]
        team.opponentID = teamData["recentResults"][0]["enemyTeam"]["id"]

    def __getPlayerID(self,player):
        params = {"name" : player.name}
        numOfTries = 0
        while numOfTries is not self.MAX_NUM_OF_RETRIES :
            response = requests.get(self.url + "player", params = params)
            if response.status_code is 200:
                playerData = response.json()
                break
            else :
                print ("Error Getting Player ID")
                print (self.url + "player?name=" + player.name)
                print (response)
                time.sleep(2.5)
                print("Trying Again...")
                numOfTries += 1
        if numOfTries is self.MAX_NUM_OF_RETRIES :
            return 0
        player.playerid = playerData["id"]



    def getAverageRoundsPerSeries(self, name, withOvertime):
        print("-------- " + name + " -----------")
        teamID = self.__getPlayerTeamID(name)
        params = {"teamid" : teamID}
        teamData = requests.get(self.url + "team", params = params).json()
        count = 0
        totalRounds = 0
        getcalls = 0
        for match in teamData["recentResults"]:
            time.sleep(1.5)
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

    def __getMatchTotals(self, matchID):
        params = {"matchid" : matchID}
        response = requests.get(self.url + "match", params = params)
        if response.status_code is 200:
            matchData = response.json()
        else:
            print("got response code of : " + str(response.status_code))
            return 0
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
        response = requests.get(self.url + "match", params = params)
        if response.status_code is 200 :
            matchData = response.json()
        else:
            print("got response code of : " + str(response.status_code))
            return 0
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
