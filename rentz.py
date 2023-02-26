from enum import Enum
import time

SLEEP_TIME = 0.5
NEW_LINE = "\n\n"

KING_OF_HEARTS = -100
QUEEN = -30
DIAMOND = -20
WHIST_HAND = 20

RENTZ = [300, 200, 100, 150, 50]

def undoDecorator(func) :
    def wrapper(*args, **kwargs) :
        # check for undo option
        undoCheck  = input("Type 'u' to undo your choice or press enter to continue: ")
        while undoCheck != "" and undoCheck != "u" :
            print("Error: Invalid choice.")
            undoCheck  = input("Type 'u' to undo your choice or press enter to continue: ")
        if undoCheck == "u" or undoCheck == "undo" :
            print(NEW_LINE)

            func(*args, **kwargs)
            return
    return wrapper

class GameType(Enum) :
    KING_OF_HEARTS = 1
    QUEENS = 2
    DIAMONDS = 3
    WHIST = 4
    RENTZ = 5
    TOTAL = 6


class Player :
    def __init__(self, name, points, lastHandPoints) :
        self.name = name
        self.points = points
        self.lastHandPoints = lastHandPoints
        self.gameTypesRemaining = [GameType.KING_OF_HEARTS, GameType.QUEENS, GameType.DIAMONDS, GameType.WHIST, GameType.RENTZ, GameType.TOTAL]
    
    def __str__(self) :
        return self.name + " has " + str(self.points) + " points."
    
    def chooseGameType(self) :
        if len(self.gameTypesRemaining) == 0 :
            return None
        else :
            #ask player to choose game type
            print("It is " + self.name + "'s turn. Choose a game type:" + NEW_LINE)

            time.sleep(SLEEP_TIME)

            outputString = "Available game types:" + NEW_LINE
            for i in range(len(self.gameTypesRemaining)) :
                outputString += self.gameTypesRemaining[i].name + " - " + str(i + 1) + ",\n"
            outputString = outputString[:-2]
            outputString += "."
            print(outputString)

            time.sleep(SLEEP_TIME)

            choice = int(input("\nPlease enter the number of the game type you would like to play: "))

            # check if choice is valid
            while choice < 1 or choice > len(self.gameTypesRemaining) :
                print("Error: Invalid choice.")

                time.sleep(SLEEP_TIME)

                print(outputString)
                choice = int(input("Please enter the number of the game type you would like to play: "))


            # check for undo option
            undoCheck  = input("Type 'u' to undo your choice or press enter to continue: ")
            while undoCheck != "" and undoCheck != "u" :
                print("Error: Invalid choice.")
                undoCheck  = input("Type 'u' to undo your choice or press enter to continue: ")
            if undoCheck == "u" or undoCheck == "undo" :
                return self.chooseGameType()

            print(NEW_LINE)
            
            gameType = self.gameTypesRemaining[choice - 1]
            return gameType
    





class Game :
    def __init__(self, players) :
        self.players = players
        self.numPlayers = len(players)
        self.gamesRemaining = len(players) * 6
        self.doubleFlag = False
        self.undoFlag = False

    def undoLastHand(self) :
        # cleans up last hand in case of an undo. Does nothing if no undo has been called on current hand.
        for player in self.players :
            player.points -= player.lastHandPoints
            player.lastHandPoints = 0

    
    def play(self) :
        while self.gamesRemaining > 0 :
            for player in self.players :
                gameType = player.chooseGameType()
                self.doubleFlag = False

                # check for double game
                dobuleCheck = input("Type 'd' to double the points or press enter to continue: ")
                while dobuleCheck != "" and dobuleCheck != "d" :
                    print("Error: Invalid choice.")
                    dobuleCheck  = input("Type 'd' to double the points or press enter to continue: ")
                if dobuleCheck == "d" or dobuleCheck == "double" :
                    self.doubleFlag = True

                player.gameTypesRemaining.remove(gameType)

                time.sleep(SLEEP_TIME)

                if gameType == GameType.KING_OF_HEARTS :
                    print("Playing King of Hearts...\n")
                    self.playKingOfHearts()
                elif gameType == GameType.QUEENS :
                    print("Playing Queens...\n")
                    self.playQueens()
                elif gameType == GameType.DIAMONDS :
                    print("Playing Diamonds...\n")
                    self.playDiamonds()
                elif gameType == GameType.WHIST :
                    print("Playing Whist...\n")
                    self.playWhist()
                elif gameType == GameType.RENTZ :
                    print("Playing Rentz...\n")
                    self.playRentz()
                elif gameType == GameType.TOTAL :
                    self.playTotal()
                else :
                    print("Error: Invalid game type.")
                
                time.sleep(SLEEP_TIME)

                outputString = "Current standings:" + NEW_LINE
                for i in range(len(self.players)) :
                    outputString += self.players[i].name + ": " + str(self.players[i].points) + " points,\n"
                outputString = outputString[:-2]
                outputString += "."
                print(outputString)

                time.sleep(SLEEP_TIME)
                print(NEW_LINE)

                self.gamesRemaining -= 1

   
    
    def playKingOfHearts(self) :
        
        # in case of undo
        self.undoLastHand()

        outputString = "Players:\n\n"

        for i in range(len(self.players)) :
            outputString += self.players[i].name + " - " + str(i + 1) + ",\n"
        outputString = outputString[:-2]
        outputString += "."

        print(outputString)

        time.sleep(SLEEP_TIME)

        choice = int(input("\nPlease enter the number of the player who received the K: "))
        while choice < 1 or choice > len(self.players) :
            print("Error: Invalid choice.")
            choice = int(input("Please enter the number of the player who received the K: "))

        self.players[choice - 1].points += KING_OF_HEARTS
        self.players[choice - 1].lastHandPoints += KING_OF_HEARTS

        if self.doubleFlag :
            self.players[choice - 1].points += KING_OF_HEARTS
            self.players[choice - 1].lastHandPoints += KING_OF_HEARTS

        undo = undoDecorator(self.playKingOfHearts)
        undo()


        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0

    def playQueens(self) :
        totalQueens = 0

        multiplier = 1
        if self.doubleFlag :
            multiplier = 2

        # in case of undo
        self.undoLastHand()

        print("For each player, enter the number of queens they received." + NEW_LINE)

        for player in self.players :
            numQueens = int(input(player.name + ": "))
            totalQueens += numQueens
            player.points += numQueens * QUEEN * multiplier
            player.lastHandPoints = numQueens * QUEEN * multiplier

        # check if total queens is 4
        if totalQueens != 4 :
            print("Error: Invalid number of queens. Re-enter the number of queens each player received.")
            for player in self.players :
                player.points -= player.lastHandPoints
                player.lastHandPoints = 0

            time.sleep(SLEEP_TIME)
            print(NEW_LINE)

            self.playQueens()
            return

        undo = undoDecorator(self.playQueens)
        undo()

        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0
        
            

    def playDiamonds(self) :
        # in case of undo
        self.undoLastHand()

        multiplier = 1
        if self.doubleFlag :
            multiplier = 2

        totalDiamonds = 0

        print("For each player, enter the number of diamonds they received." + NEW_LINE)

        for player in self.players :
            numDiamonds = int(input(player.name + ": "))
            totalDiamonds += numDiamonds
            player.points += numDiamonds * DIAMOND * multiplier
            player.lastHandPoints = numDiamonds * DIAMOND * multiplier

        # check if total diamonds is correct
        if totalDiamonds != 2 * self.numPlayers :
            print("Error: Invalid number of diamonds. Re-enter the number of diamonds each player received.")
            for player in self.players :
                player.points -= player.lastHandPoints
                player.lastHandPoints = 0

            time.sleep(SLEEP_TIME)
            print(NEW_LINE)

            self.playDiamonds()
            return
        
        # check for undo option
        undo = undoDecorator(self.playDiamonds)
        undo()

        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0
        
    def playWhist(self) :
        # in case of undo
        self.undoLastHand()

        totalHands = 0

        multiplier = 1
        if self.doubleFlag :
            multiplier = 2

        # get number of hands each player has won
        print("For each player, enter the number of hands they won." + NEW_LINE)

        for player in self.players :
            numHands = int(input(player.name + ": "))
            totalHands += numHands
            player.points += numHands * WHIST_HAND * multiplier
            player.lastHandPoints = numHands * WHIST_HAND * multiplier
        
        # check if total hands is correct
        if totalHands != 8 :
            print("Error: Invalid number of hands. Re-enter the number of hands each player won.")
            for player in self.players :
                player.points -= player.lastHandPoints
                player.lastHandPoints = 0

            time.sleep(SLEEP_TIME)
            print(NEW_LINE)

            self.playWhist()
            return
        
        # check for undo option
        undo = undoDecorator(self.playWhist)
        undo()

        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0
        

    def playRentz(self) :
        placeStrings = ["first", "second", "third", "fourth", "fifth", "sixth"]

        # in case of undo
        self.undoLastHand()

        multiplier = 1
        if self.doubleFlag :
            multiplier = 2

        outputString = "Players:\n\n"

        for i in range(len(self.players)) :
            outputString += self.players[i].name + " - " + str(i + 1) + ",\n"
        outputString = outputString[:-2]
        outputString += "."

        print(outputString)

        time.sleep(SLEEP_TIME)

        for i in range(self.numPlayers):
            choice = int(input("\nPlease enter the number of the player who came in " + placeStrings[i] + ": "))
            while choice < 1 or choice > len(self.players) :
                print("Error: Invalid choice.")
                choice = int(input("Please enter the number of the player who came in " + placeStrings[i] + ": "))

            self.players[choice - 1].points += RENTZ[i] * multiplier
            self.players[choice - 1].lastHandPoints += RENTZ[i] * multiplier

        undo = undoDecorator(self.playRentz)
        undo()

        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0

    def playTotal(self) :
        print("Playing Total")

        # in case of undo
        self.undoLastHand()

        totalPoints = 8 * WHIST_HAND * -1 + 2 * self.numPlayers * DIAMOND + 4 * QUEEN + KING_OF_HEARTS

        if self.doubleFlag :
            totalPoints *= 2


        print("Total points: " + str(totalPoints) + NEW_LINE)

        print("For each player, enter the number of points they received. If you want it to be " + 
        + "automatically calculated enter 'x'. Note: This can only be done for 1 player" + NEW_LINE)
        
        xPos = -1
        for i in range(len(self.players)) :
            points = input(self.players[i].name + ": ")
            if points == "x" :
                if xPos != -1 :
                    print("Error: Already entered 'x' for " + self.players[xPos].name + ". Please enter a number.")

                    time.sleep(SLEEP_TIME)
                    print(NEW_LINE)
                    points = int(input(self.players[i].name + ": "))

                    self.players[i].points += points
                    self.players[i].lastHandPoints += points
                    totalPoints -= points
                else :
                    xPos = i
                    continue
            else :
                points = int(points)
                self.players[i].points += points
                self.players[i].lastHandPoints += points
                totalPoints -= points

        if xPos != -1 :
            self.players[xPos].points += totalPoints
            self.players[xPos].lastHandPoints += totalPoints
        else :
            if totalPoints != 0 :
                print("Error: Invalid number of points. Re-enter the number of points each player received.")
                for player in self.players :
                    player.points -= player.lastHandPoints
                    player.lastHandPoints = 0

                time.sleep(SLEEP_TIME)
                print(NEW_LINE)

                self.playTotal()
                return

        undo = undoDecorator(self.playTotal)
        undo()

        print(NEW_LINE)

        # clean up last hand
        for player in self.players :
            player.lastHandPoints = 0



def main() :
    players = []
    numPlayers = int(input("How many players are there? "))
    # if numPlayers < 3 or numPlayers > 6 :
    #     print("Error: Invalid number of players.")
    #     return
    print(NEW_LINE)
    for i in range(numPlayers) :
        name = input("Enter the name of player " + str(i + 1) + ": ")
        print(NEW_LINE)
        players.append(Player(name, 0, 0))
    
    game = Game(players)
    game.play()



if __name__ == "__main__" :
    main()
                

        
            