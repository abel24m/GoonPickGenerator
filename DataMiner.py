
import requests
import time

class DataMiner(object):

    url = "https://whispering-bayou-49673.herokuapp.com/"
    MAPS_MINIMUM = 0
    NUMBER_OF_MATCHES = 8
    OVERTIME_SCORE = 16


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
        playerData = requests.get(self.url + "player", params = params).json()
        kpr = playerData["statistics"]["killsPerRound"]
        return kpr

    def getAverageRoundsPerSeries(self, name, withOvertime):
        print("-------- " + name + " -----------")
        print("Getting Average Rounds with Overtime : " + str(withOvertime))
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

    def __getPlayerTeamID(self,name):
        params = {"name" : name}
        playerData = requests.get(self.url + "player", params = params).json()
        teamName = playerData["team"]["name"]
        teamID = playerData["team"]["id"]
        return teamID

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
