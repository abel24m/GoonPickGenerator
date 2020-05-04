
import requests
import time

class DataMiner(object):

    url = "https://whispering-bayou-49673.herokuapp.com/"
    MAPS_MINIMUM = 1
    NUMBER_OF_MATCHES = 10
    OVERTIME_SCORE = 16
    specialCases = [2340256]


    def __init__(self):
        super(DataMiner, self).__init__()

    def getPlayerKpr(self,name):
        params = {"name" : name}
        playerData = requests.get(self.url + "player", params = params).json()
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
                                print(parsedResults[0])
                                totalRounds += int(rounds)
                if count >= self.MAPS_MINIMUM:
                    break;
        return totalRounds
