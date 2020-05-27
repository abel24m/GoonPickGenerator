from Sport_Structures.Player import Player

class IO_Manager(object):

    def __init__(self):
        self.rowStart = 1
        self.numOfMaps = 1


    # Initialize the CSGO pick generator.
    # Request the major metadata for the the rest of the program
    def init_CSGO(self, csgo_metaData):
        print ("\n\nStarting CSGO Pick Generator...\n\n")

    #Request the main data that will be used to produce results for
    # In this case we need the names of the players and the projection we will be going against
    def request_CSGO_MetaData(self, csgo_metaData):
        players = []    #List of players that are in prizepicks and we will be building projections for

        # Check to make sure the response is a valid one
        # We want a positive number.
        while True:
            numOfPlayers = input("How many players will I be generating picks for : ")
            if not numOfPlayers.isnumeric():
                print("Input needs to be a number...Try Again")
            elif int(numOfPlayers) <= 0:
                print("Input needs to be a positive number...Try Again")
            else:
                numOfPlayers = int(numOfPlayers)
                break

        # Request the names and prjections of the Players
        # We use the number the user inputed for the iteration
        # We create a player object and write all players to the csgo meta data dictionary
        for count in range(0,numOfPlayers) :
            name = input("\nPlease enter a name : ")
            numOfMaps = int(input("\nNumber of Maps being played : "))
            prizepick = float(input("\nPlease enter the PrizePick projection : "))
            player = Player(name, prizepick, numOfMaps)
            players.append(player)
        csgo_metaData["players"] = players
