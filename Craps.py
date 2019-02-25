# Craps.py

import numpy as np
from matplotlib import pyplot as plt

# Pass Bets
#   Pass line
#   Pass Line odds
#   Don't pass
#   Don't Pass odds`

# Come Bets
#   Come 4-10
#   Come odds 4-10
#   Don't Come 4-10
#   Don't Come odds 4-10

# Multi-Roll Bets
#   Place 4-10
#   Hard way
#   Big 6/8

# Single-Roll Bets
#   Come
#   Don't Come
#   2
#   3
#   11
#   12
#   Hi-lo
#   Any Craps
#   C & E
#   Any Seven
#   Field

# Lists of bets by type
pass_list = ["Pass", "Pass odds", "Don't Pass", "Don't Pass odds"]
come_list = ["Come 4", "Come 5", "Come 6", "Come 8", "Come 9", "Come 10",
"Come odds 4", "Come odds 5", "Come odds 6", "Come odds 8", "Come odds 9",
"Come odds 10", "Don't Come 4", "Don't Come 5", "Don't Come 6", "Don't Come 8",
"Don't Come 9", "Don't Come 10", "Don't Come odds 4", "Don't Come odds 5",
"Don't Come odds 6", "Don't Come odds 8", "Don't Come odds 9",
"Don't Come odds 10"]
multi_list = ["Place 4", "Place 5", "Place 6", "Place 8", "Place 9",
"Place 10", "Hard 4", "Hard 6", "Hard 8", "Hard 10", "Big 6", "Big 8"]
single_list = ["Come", "Don't Come", "2", "3", "11", "12", "Any Craps",
"Any Seven", "Field"]
house_edge = [1.41, 1.36, 6.67, 4, 1.52, 1.52, 4, 6.67, 11.11, 9.09, 9.09, 11.11, 9.09, 9.09, 1.41, 1.37, 13.89, 11.11, 11.11, 13.89, 11.11, 16.67, 2.78]

# Dictionary of all bets for looking up bet location indices
all_bets = dict((v, k) for k, v in dict(enumerate(pass_list + come_list + multi_list + single_list)).items())

# Dictionary of bets you can lay money on (not the Come/Don't Come numbers or
# odds)
play_bets = pass_list[::2] + multi_list + single_list
# List of corresponding indices of play_bets
play_bet_locs = [all_bets[a] for a in play_bets]
play_bets_dict = dict(zip(play_bets, range(23)))


# Dictionaries of bets by type
pass_bets = dict(enumerate(pass_list))
come_bets = dict(enumerate(come_list))
multi_bets = dict(enumerate(multi_list))
single_bets = dict(enumerate(single_list))
"""
Pass bets
0: 'Pass',                  1: 'Pass odds',             2: "Don't Pass",
3: "Don't Pass odds",

Come bets
0: 'Come 4',                1: 'Come 5',                2: 'Come 6',
3: 'Come 8',                4: 'Come 9',                5: 'Come 10',
6: 'Come odds 4',           7: 'Come odds 5',           8: 'Come odds 6',
9: 'Come odds 8',           10: 'Come odds 9',          11: 'Come odds 10',
12: "Don't Come 4",         13: "Don't Come 5",         14: "Don't Come 6",
15: "Don't Come 8",         16: "Don't Come 9",         17: "Don't Come 10",
18: "Don't Come odds 4",    19: "Don't Come odds 5",    20: "Don't Come odds 6",
21: "Don't Come odds 8",    22: "Don't Come odds 9",    23: "Don't Come odds 10",

Multi-roll bets
0: 'Place 4',               1: 'Place 5',               2: 'Place 6',
3: 'Place 8',               4: 'Place 9',               5: 'Place 10',
6: 'Hard 4',                7: 'Hard 6',                8: 'Hard 8',
9: 'Hard 10',               10: 'Big 6'                 11: 'Big 8'

Single-roll bets
0: 'Come',                  1: "Don't Come",            2: '2',
3: '3',                     4: '11',                    5: '12',
6: "Any Craps",             7: 'Any Seven',             8: 'Field'
"""

# Lists of different collections of related numbers
points_low = [4, 5, 6]
points_high = [8, 9, 10]
points = points_low + points_high
craps = [2, 3, 12]

# Payouts
# Odds payouts for Pass/Don't Pass line corresponding to the 6 points
pass_odds = [2, 3/2, 6/5, 6/5, 3/2, 2]
dont_odds = [1/2, 2/3, 5/6, 5/6, 2/3, 1/2]
# Payouts for bets by type (Pass/Don't Pass odds are calculated below when
# applicable, Field payouts also handled below )
pass_payouts = [1]*4
come_payouts = [1]*6 + pass_odds + [1]*6 + dont_odds
multi_payouts = [9/5, 7/5, 7/6, 7/6, 7/5, 9/5, 7, 9, 9, 7, 1, 1]
single_payouts = [1, 1, 30, 15, 15, 30, 7, 4, 1]

# Whether or not bets are removed from the table when they are won
# 1 would clear when won, 0 would remain on table when won
# clear_when_win = [1]*28 + [0]*6 + [1]*4 + [0]*2 + [1]*9
clear_when_win = [1]*49



class Player:
    """Class for players that stores player's name, starting amount, total
    amount, total winnings, and total losses."""

    def __init__(self, name, initial):
        """Initializes different attributes for the player.

        Parameters:
            name (str): The player's name
            initial (int): The amount of money the player is playing with

        Attributes:
            total (int): The player's total money at a given point in time
            winnings (int): Total amount of money won (summed roll by roll)
            losses (int): Total amount of money lost (summed roll by roll)
        """

        self.name = name
        self.initial = initial
        self.total = initial
        self.winnings = 0
        self.losses = 0

    def winnings(self, amount_won):
        """Adds the amount of money won to the players winnings.

        Parameters:
            amount_won (int): The amount won to be added to the player's
                total winnings
        """
        self.winnings += amount_won

    def losses(self):
        """Subtracts the amount of money lost from the players losses.

        Parameters:
            amount_lost (int): The amount lost to be subtracted from
            the player's total losses
        """
        self.losses += amount_lost

    def bet_loc(self):
        """Prints all bets that the player has money on and the amounts the
        player currently has on each betself.

        Example:
            Jon's bets:
                Pass Line       5
                Pass odds       15
                Field           5
                Come 6          5
                Hard 8          1
        """
        pass


class Table:
    """Class for the table describes table minimum, table maximum, and Field
    payout on 12. Keeps track of table condition including status of the button
    and current point and also keeps track of players at table, their bet
    locations and amounts, and totals."""

    def __init__(self, field = 3, print = False, table_min = 5, table_max = 5000):
        """Initializes the attributes of the table.

        Parameters:
            min (int): The minimum required bet for the table
            max (int): The maximum required bet for the table
            button (str): The button's status, either "OFF" or "ON"
            players (list): A list of each of the players at the table
            print (bool): A boolean value that determines whether or not to
                print out the table status after each roll
            field_payouts (list): The payouts when the field wins;
                1x for 3, 4, 9, 1, 11;
                2x for 2;
                either 2x or 3x for 12
        """
        self.min = table_min
        self.max = table_max
        self.button = "OFF"
        self.players = []
        self.print = print
        if field == 3:
            self.field_payouts = [1, 2, 3]
        else:
            self.field_payouts = [1, 2, 2]

    def button_on(self, point):
        """When the come-out point is established. Sets the point and changes
        the button's status to "ON".
        """
        self.button = "ON"
        self.point = point

    def point_hits(self):
        """When the point hits and the Pass line wins. Sets the button's status
        to "OFF" and prints out "POINT HITS" if the table is set to print.
        """
        self.button = "OFF"
        if self.print:
            print("POINT HITS")

    def button_status(self):
        """Prints the status of the table: the button's status and the point
        when applicable.
        """
        if self.button == "OFF":
            print("The button is OFF")
        else:
            print("The button is ON the " + str(self.point))

    def seven_out(self):
        """When the button is "ON" a point and a 7 is rolled before the point
        hits. Sets the button status to "OFF" and prints out "SEVEN OUT" if the
        table is set to print.
        """
        self.button = "OFF"
        if self.print:
            print("SEVEN OUT")

    def add_player(self, player):
        """Adds a player to the table and adds a row of bets to the array of all
        player's bets as well as adds a place to the totals of the players at
        the table.
        """
        self.players.append(player)
        if len(self.players) == 1:
            self.bets = np.zeros((1, 49))
            self.totals = np.array([self.players[0].total])
        else:
            self.bets = np.vstack((self.bets, np.zeros((1, 49))))
            self.totals = np.concatenate((self.totals, np.array([self.players[-1].total])))


def roll_dice():
    """Randomly generates two integers between 1 and 6 to simulate rolling 2
    dice

    Returns:
        total (int): The value of the roll
        roll (list): The values of the two individual dice
    """
    roll = np.random.randint(1, 7, 2)
    total = sum(roll)
    return total, roll


def shoot(table):
    """Gets a new dice roll, calculates all of the bets that win and their
    payouts depending on the roll and the table status, and calculates the
    winnings and losses of all of the players.

    Parameters:
        table (Table): The table object that is being played on

    Return:
        table (Table): The table object after having updated the totals and
            table status
    """
    # The "_bets" lists: 0 - loses, 1 - wins, 2 - remains on the table
    # The "_payouts" lists contains the payouts for each bet
    # Initializes the payouts and bets lists
    pass_bets = [2]*4
    come_bets = [2]*24
    multi_bets = [2]*12
    single_bets = [2]*2 + [0]*7
    # Resets the Field payouts according to the table
    field_payouts = table.field_payouts
    single_payouts[8] = field_payouts[0]

    # Roll the dice
    roll, dice = roll_dice()
    # Prints the roll value and table status if the table is set to print
    if table.print:
        table.button_status()
        print(roll)

    # Sets the bets that win/lose/stay if the button is "ON"
    if table.button == "ON":
        # Seven Out
        if roll == 7:
            # Changes the button status
            table.seven_out()
            # The Pass Line loses and the Don't Pass Line wins
            pass_bets = [0, 0, 1, 1]
            # The Come bets lose and the Don't Come bets win
            come_bets = [0]*12 + [1]*12
            # All Multi bets lose
            multi_bets = [0] * 12
            # Come bet wins
            single_bets[0] = 1
            # Don't Come bet loses
            single_bets[1] = 0
            # Any Seven wins
            single_bets[7] = 1
            # Sets the Don't Pass Line odds payout according to value of the
            # point rolled
            for i, v in enumerate(points):
                if table.point == v:
                    pass_payouts[3] = dont_odds[i]
        # Sets the bets win/lose/stay if the roll is a 4, 5, 6, 8, 9, 10
        elif roll in points:
            # Sets the best that win/lose/stay if the point hits
            if roll == table.point:
                # Pass Line Wins and Don't Pass Line Loses
                pass_bets = [1, 1, 0, 0]
                # Sets the Pass Line odds payout according to value of the
                # point rolled
                for i, v in enumerate(points):
                    if roll == v:
                        pass_payouts[1] =  pass_odds[i]
                # Changes the table status
                table.point_hits()
            # If the roll is a 4
            if roll == 4:
                # Come 4 and Come 4 odds win
                come_bets[0] = 1
                come_bets[6] = 1
                # Don't Come 4 and Don't Come 4 odds lose
                come_bets[12] = 0
                come_bets[18] = 0
                # Place 4 wins
                multi_bets[0] = 1
                # Hard 4
                if dice[0] == dice[1]:
                    # Hard 4 wins if double 2s are rolled
                    multi_bets[6] = 1
                else:
                    # Hard 4 loses if a soft 4 is rolled
                    multi_bets[6] = 0
                # Field wins
                single_bets[8] = 1
            elif roll == 5:
                # Come 5 and Come 5 odds win
                come_bets[1] = 1
                come_bets[7] = 1
                # Don't Come 5 and Don't Come 5 odds lose
                come_bets[13] = 0
                come_bets[19] = 0
                # Place 5 wins
                multi_bets[1] = 1
            elif roll == 6:
                # Come 6 and Come 6 odds win
                come_bets[2] = 1
                come_bets[8] = 1
                # Don't Come 6 and Don't Come 6 odds lose
                come_bets[14] = 0
                come_bets[20] = 0
                # Place 6 wins
                multi_bets[2] = 1
                # Big 6 wins
                multi_bets[10] = 1
                # Hard 6
                if dice[0] == dice[1]:
                    # Hard 6 wins if double 3s are rolled
                    multi_bets[7] = 1
                else:
                    # Hard 6 loses if a soft 3 is rolled
                    multi_bets[7] = 0
            elif roll == 8:
                # Come 8 and Come 8 odds win
                come_bets[3] = 1
                come_bets[9] = 1
                # Don't Come 8 and Don't Come 8 odds lose
                come_bets[15] = 0
                come_bets[21] = 0
                # Place 8 wins
                multi_bets[3] = 1
                # Big 8 wins
                multi_bets[11] = 1
                # Hard 8
                if dice[0] == dice[1]:
                    # Hard 8 wins if double 4s are rolled
                    multi_bets[8] = 1
                else:
                    # Hard 8 loses if a soft 8 is rolled
                    multi_bets[8] = 0
            elif roll == 9:
                # Come 9 and Come 9 odds win
                come_bets[4] = 1
                come_bets[10] = 1
                # Don't Come 9 and Don't Come 9 odds lose
                come_bets[16] = 0
                come_bets[22] = 0
                # Place 9 wins
                multi_bets[4] = 1
                # Field wins
                single_bets[8] = 1
            elif roll == 10:
                # Come 10 and Come 10 odds win
                come_bets[5] = 1
                come_bets[11] = 1
                # Don't Come 10 and Don't Come 10 odds lose
                come_bets[17] = 0
                come_bets[23] = 0
                # Place 10
                multi_bets[5] = 1
                # Hard 10
                if dice[0] == dice[1]:
                    # Hard 10 wins if double 5s are rolled
                    multi_bets[9] = 1
                else:
                    # Hard 10 loses if a soft 10 is rolled
                    multi_bets[9] = 0
                # Field wins
                single_bets[8] = 1
        # If a 2 or 3 is rolled
        elif roll == 2 or roll == 3:
            # Come bet loses
            single_bets[0] = 0
            # Don't Come bet wins
            single_bets[1] = 1
        elif roll == 11:
            # Come bet wins
            single_bets[0] = 1
            # Don't Come bet loses
            single_bets[1] = 0
        elif roll == 12:
            # Come bet loses
            single_bets[0] = 0
            # Don't Come pushes
            single_bets[1] = 2
    # Sets the bets that win/lose/stay when the button is "OFF"
    # It is assumed that all bets are not working when the button is "OFF"
    else:
        # If a point number is rolled on the come-out roll
        if roll in points:
            # The button status is changed
            table.button_on(roll)
            # The pass bets are initialized
            pass_bets = [2]*4
            # If the roll is a 4
            if roll == 4:
                # Field wins
                single_bets[8] = 1
                # Come 4 wins
                come_bets[0] = 1
                # Come 4 odds are not working
                come_bets[6] = 2
                # Don't Come and Don't Come odds lose
                come_bets[12] = 0
                come_bets[18] = 0
                # Hard 4
                if dice[0] == dice[1]:
                    # Hard 4 wins if double 2s are rolled
                    multi_bets[6] = 1
                else:
                    # Hard 4 loses if a soft 4 is rolled
                    multi_bets[6] = 0
            # If the roll is a 5
            elif roll == 5:
                # Come 5 wins
                come_bets[1] = 1
                # Come 5 odds are not working
                come_bets[7] = 2
                # Don't Come 5 and Don't Come 5 odds lose
                come_bets[13] = 0
                come_bets[19] = 0
            elif roll == 6:
                # Big 6 wins
                multi_bets[10] = 1
                # Come 6 wins
                come_bets[2] = 1
                # Come 6 odds are not working
                come_bets[8] = 2
                # Don't Come 6 and Don't Come 6 odds lose
                come_bets[14] = 0
                come_bets[20] = 0
                # Hard 6
                if dice[0] == dice[1]:
                    # Hard 6 wins if double 3s are rolled
                    multi_bets[7] = 1
                else:
                    # Hard 6 loses if a soft 6 is rolled
                    multi_bets[7] = 0
            # If an 8 is rolled
            elif roll == 8:
                # Big 8 wins
                multi_bets[11] = 1
                # Come 8 wins
                come_bets[3] = 1
                # Come 8 odds are not working
                come_bets[9] = 2
                # Don't Come 8 and Don't Come 8 odds lose
                come_bets[15] = 0
                come_bets[21] = 0
                # Hard 8
                if dice[0] == dice[1]:
                    # Hard 8 wins if double 4s are rolled
                    multi_bets[8] = 1
                else:
                    # Hard 8 loses if a soft 8 is rolled
                    multi_bets[8] = 0
            # If a 9 is rolled
            elif roll == 9:
                # Field wins
                single_bets[8] = 1
                # Come 9 wins
                come_bets[4] = 1
                # Come 9 odds are not working
                come_bets[10] = 2
                # Don't Come 9 and Don't Come 9 odds lose
                come_bets[16] = 0
                come_bets[22] = 0
            # If a 10 is rolled
            elif roll == 10:
                # Field wins
                single_bets[8] = 1
                # Come 10 wins
                come_bets[5] = 1
                # Come 10 odds are not working
                come_bets[11] = 2
                # Don't Come 10 and Don't Come 10 odds lose
                come_bets[17] = 0
                come_bets[23] = 0
                # Hard 10
                if dice[0] == dice[1]:
                    # Hard 10 wins if double 5s are rolled
                    multi_bets[9] = 1
                else:
                    # Hard 10 loses if a soft 10 is rolled
                    multi_bets[9] = 0
        # If the come-out roll is a 7
        elif roll == 7:
            # Pass Line wins, Don't Pass Line loses
            pass_bets = [1, 2, 0, 2]
            # Any Seven wins
            single_bets[7] = 1
            # All Come lose, Come odds are not working, and Don't Come and Don't
            # Come odds win
            come_bets = [0]*6 + [2]*6 + [1]*6 + [1]*6
            # Place bets are not working, Big 6/8 and all hard ways lose
            multi_bets = multi_bets[0:6] + [0]*6
        # If the come-out roll is a 2 or 3
        elif roll == 2 or roll == 3:
            # Pass Line loses and Don't Pass line wins
            pass_bets = [0, 2, 1, 2]
        # If the come-out roll is a 12
        elif roll == 12:
            # Pass Line loses
            pass_bets = [0, 2, 2, 2]
        # If the come-out roll is an 11
        else:
            # Pass Line wins and Don't Pass Line loses
            pass_bets = [1, 2, 0, 2]
    # Sets single bets that win/lose/stay
    # If the roll is a 2
    if roll == 2:
        # 2 wins
        single_bets[2] = 1
        # Any Craps wins
        single_bets[6] = 1
        # Field wins
        single_bets[8] = 1
        # Field payout is double
        single_payouts[8] = field_payouts[1]
    # If the roll is a 3
    elif roll == 3:
        # 3 wins
        single_bets[3] = 1
        # Any Craps wins
        single_bets[6] = 1
        # Field wins
        single_bets[8] = 1
    # If the roll is an 11
    elif roll == 11:
        # 11 wins
        single_bets[4] = 1
        # Field wins
        single_bets[8] = 1
    # If the roll is a 12
    elif roll == 12:
        # 12 wins
        single_bets[5] = 1
        # Any Craps wins
        single_bets[6] = 1
        # Field wins
        single_bets[8] = 1
        # Field payout is double or triple depending on table
        single_payouts[8] = field_payouts[2]

    # Creats an array of all the bets with 1 - win, 0, lose, 2 - unchanged
    bets = np.asarray(pass_bets + come_bets + multi_bets + single_bets)
    # Creates an array of all of the payouts of the respective bets
    payouts = np.asarray(pass_payouts + come_payouts + multi_payouts + single_payouts)
    # Creates an array with the payouts of only the bets that win with 0s
    # everywhere else
    roll_payouts = (bets * [bets == 1]) * payouts
    # Calculates the winnings for all players
    winnings = np.ndarray.flatten(table.bets @ roll_payouts.T)
    # Calculates the losses for all players
    losses = np.sum(table.bets.T[bets == 0].T, axis = 1)
    # Removes all bets that lost from the table
    table.bets.T[bets == 0] = 0
    # Calculates the totals of all players by adding their winnings and
    # subtracting their losses
    table.totals = table.totals + winnings - losses

    # Creates an array with 1 - lose, 0 - win or remains unchanged
    bets[bets == 2] = 0
    # Calculates which bets that won need to be cleared
    clear = clear_when_win * bets
    # Creates a mask where 1 - doesn't clear, 0 - clears
    mask = [clear == 0]
    # Clears the appropriate bets from the table
    table.bets = table.bets * mask

    # Move's players Come bets to the corresponding point
    # If the roll is a 4, 5, 6, 8, 9, or 10 and there are bets on the Come/Don't
    # Come
    if roll in points and np.sum(table.bets[:,40]) > 0 or roll in points and np.sum(table.bets[:,41]) > 0:
        # Iterates through each player
        for i in range(table.bets.shape[0]):
            # If the ith player has bet on the Come
            if table.bets[i][40] != 0:
                # Iterates through each of the points
                for j, v in enumerate(points):
                    # Checks for the roll value
                    if roll == v:
                        # Moves the player's Come bet to the appropriate point
                        table.bets[i][j + 4] = table.bets[i][j + 4] + table.bets[i][40]
                        # Clears the Come bet
                        table.bets[i][40] = 0
            # If the ith player has bet on the Don't Come
            if table.bets[i][41] != 0:
                # Iterates through each of the points
                for j, v in enumerate(points):
                    # Checks for the roll value
                    if roll == v:
                        # Moves the player's Don't Come bet to the appropriate
                        # point
                        table.bets[i][j + 16] = table.bets[i][j + 16] + table.bets[i][41]
                        # Clears the Don't Come bet
                        table.bets[i][41] = 0

    return table, winnings, losses

def single_player_repeating(name, initial, bet, bet_amount, max_rolls = 50000, plot = True):
    """A single player plays the same bet until they lose.

    Parameters:
        name (str): Player's name
        initial (int): Player's starting amount
        bet (str): The name of the bet the player will be playing
        bet_amount (int): The amount to bet each roll
    """
    # Initializes the Table and variables
    A = Table()
    A.add_player(Player(name, initial))
    initial = str(A.totals[0])
    bet_loc = all_bets[bet]
    totals = []
    i = 0
    # Plays until player is broke or max_rolls have been played
    while np.sum(A.totals) > 0 and i < max_rolls:
        A, win, loss = shoot(A)
        # Places the bet if there is not one already there
        if A.bets[0][bet_loc] == 0:
            A.bets[0][bet_loc] += bet_amount
        totals.append(A.totals[0])
        i += 1
    # Plots a line graph of the player's totals
    if plot:
        plt.plot(totals)
        plt.title("Playing the " + bet + "\nInitial: \$" + initial + "     Bet: \$" + str(bet_amount))
        plt.xlabel("Rolls")
        plt.ylabel("Total")
        plt.show()
    # Returns the current total, used in other functions for testing strategies
    else:
        return A.totals[0]

def multi_players_repeating():
    """Multiple players play the same bet until they lose. Running this function
    will prompt for each players name, number of players, name, starting amount,
    bet, and bet amount and finally run until all players are broke displaying
    a graph of their totals.
    """
    # Prompts user for Table type
    twelve, num_players = 0, ""
    while twelve != 2 and twelve != 3:
        twelve = int(input("Field payout on 12? "))
        try:
            if twelve != 2 and twelve != 3:
                print(ValueError("Payout on 12 must be 2 or 3"))
        except:
            pass
    # Prompts user for number of players
    while type(num_players) != int:
        try:
            num_players = int(input("How many Players? "))
        except:
            print("Must be an integer")
    # Initializes variables
    A = Table(twelve)
    bets = []
    bet_locs = []
    bet_amounts = []
    totals = []
    # Prompts for player's names, starting amounts, bets, and bet amounts
    for i in range(num_players):
        name = input("Player " + str(i + 1) + " name: ")
        initial = int(input("Player " + str(i + 1) + " initial amount: "))
        A.add_player(Player(name, initial))
        bets.append(input("Player " + str(i + 1) + " bet: "))
        bet_locs.append(all_bets[bets[i]])
        bet_amounts.append(int(input("Player " + str(i + 1) + " bet amount: ")))
    totals = []
    i = 0
    # Runs until each player goes broke
    while np.sum(A.totals) > 0:
        A, win, loss = shoot(A)
        # Places each player's bet if they don't have one on the table
        for j in range(len(A.players)):
            if A.totals[j] > 0:
                if A.bets[j][bet_locs[j]] == 0:
                    A.bets[j][bet_locs[j]] += bet_amounts[j]
        totals.append(A.totals)
        i += 1
    # Plots the graphs of each player's totals
    for i in range(len(A.players)):
        plt.plot(np.asarray(totals)[:,i], label = A.players[i].name + ": " + bets[i])
    plt.title("Player Totals")
    plt.xlabel("Rolls")
    plt.ylabel("Total")
    plt.legend()
    plt.show()

def play_all_repeating(max_rolls, plot = True):
    """A single player plays the same bet until they lose. Each player starts
    with $500 and bets $50 each roll.

    Parameters:
        max_rolls (int): The maximum number of rolls to simulate
        plot (bool):  When plot is True, a graph of each player's totals is
            displayed. When plot is False, returns the number of rolls each
            player played before going broke. Used for stats_all_repeating()
            function.

    Returns:
        roll_counts (np.array): Returned only when plot is False, an array
            corresponding to each of the playable bets with the number of rolls
            that each player played before going broke
    """
    # Initializes the table and bets for all players
    A = Table()
    bet_locs = []
    bet_amounts = [50] * 23
    for i in range(23):
        A.add_player(Player("", 500))
        bet_locs.append(play_bet_locs[i])
    totals = []
    i = 0
    while np.sum([A.totals > 50]) and i <= max_rolls:
        # Places each player's bet
        for j in range(23):
            if A.totals[j] > 0:
                # Takes into account the money that Come has elsewhere on the
                # table so that they don't bet more money than they have
                if j == 14:
                    if A.button == "ON" and np.sum(A.bets[j][4:9]) <= A.totals[j] - bet_amounts[j]:
                        A.bets[j][bet_locs[j]] += bet_amounts[j]
                elif j == 15:
                    if A.button == "ON" and np.sum(A.bets[j][16:21]) <= A.totals[j] - bet_amounts[j]:
                        A.bets[j][bet_locs[j]] += bet_amounts[j]
                elif A.bets[j][bet_locs[j]] == 0:
                    if A.totals[j] >= bet_amounts[j]:
                        A.bets[j][bet_locs[j]] += bet_amounts[j]
        totals.append(A.totals)
        A, win, loss = shoot(A)
        i += 1
    totals = np.asarray(totals)
    # Plots a graph of all 23 bets and reports the highest winning bet
    if plot:
        max_loc = np.argmax(totals)
        best_bet = play_bets[max_loc%23]
        plt.subplot(111)
        plt.suptitle("Player Totals")
        styles = ['-', '--', '-.', ':']
        marker = ['+', ',', '.', '1', '2', '3', '4', 'o', 'v']
        for i in range(len(A.players)):
            plt.plot(totals[:,i], styles[i%4], label = play_bets[i], marker = marker[i%7])
        plt.title("The bet that went up the most was the " + best_bet + " with $" + str(round(np.max(totals))) + " after " + str(np.argmax(totals[:,max_loc%23])) + " rolls", fontsize = 8)
        plt.xlabel("Rolls")
        plt.ylabel("Total ($)")
        plt.legend(prop={'size': 6})
        plt.show()
    # Retuns data collected for the stats_all_repeating() function
    else:
        # Finds the max winnings and rolls after which max winnings were reached
        max_winnings_rolls = np.zeros(23)
        max_winnings = np.zeros(23)
        for i in range(23):
            max_winnings_rolls[i] = np.argmax(totals[:,i])
            max_winnings[i] = np.max(totals[:,i])
        rolls = np.sum(totals > 50, axis = 0)
        best_bet = np.argmax(totals)%23
        return rolls, max_winnings_rolls, max_winnings, best_bet

def stats_all_repeating(iterations):
    """Runs the play_all_repeating() function until all players (representing
    all of the different bets) have run out of money generating iterations
    random samples for statistical analysis.

    Parameters:
        iterations (int): The number of random samples to be generated

    Returns:
        rolls (np.array): The number of rolls before each bet went broke for
            each iteration
        max_win (np.array): The maximum total amount each player reached in each
            iteration
        max_win_rolls (np.array): The number of rolls after which each player
            reached their maximum total amount for each iteration
        best_bet (np.array): The bet in each iteration that reached the highest
            total amount
    """
    # Intiializes the arrays to be returned
    rolls = np.empty(iterations, dtype='object')
    max_win_rolls = np.empty(iterations, dtype='object')
    max_win = np.empty(iterations, dtype='object')
    best_bet = np.empty(iterations, dtype='object')
    # Updates each of the arrays with the data from iterations random samples
    for i in range(iterations):
        rolls[i], max_win_rolls[i], max_win[i], best_bet[i] = play_all_repeating(100000, False)
        # Lets us know the progress of the function for very large iterations
        print(i)
    return np.stack(rolls), np.stack(max_win), np.stack(max_win_rolls), np.stack(best_bet)

def max_single_bet(bet, opt_rolls):
    """An implementation of the strategy of betting the same bet for the input
    optimum number of rolls before cashing out.

    Plots a graph of of the mean winnings for 2000 samples of this strategy.
    This is done for 7 different roll values (the middle/fourth being
    the actual 'optimum' roll value) for comparison.

    Parameters:
        bet (str): The name of the bet the player will be playing
        opt_rolls (int): Calculated from the stats_all_repeating function, this
            is the average number of rolls before the bet reaches its maximum
            winnings
    """
    # Gets various roll values with the 'optimal' roll value in the middle
    opt_rolls_dom = np.linspace(0, opt_rolls, 7)*2
    avgs = []
    # Runs for each of the roll values in opt_rolls_dom
    for i in range(7):
        totals = []
        # Runs 2000 random samples to get a stable mean total after the
        # specified number of rolls
        for j in range(2000):
            totals.append(single_player_repeating("Name", 500, "12", 50, max_rolls = opt_rolls_dom[i], plot = False))
        avgs.append(np.mean(np.asarray(totals)))
    # Plots a graph of the mean totals after each number of rolls
    plt.plot(opt_rolls_dom, np.asarray(avgs) - 500)
    plt.title("Average Winnings Playing the " + bet)
    plt.plot([opt_rolls, opt_rolls], [min(avgs) - 500, max(avgs) - 500], label = "Optimum")
    plt.xlabel("Rolls")
    plt.ylabel("Winnings $")
    plt.legend(loc = 1)
    plt.show()

"""=========================================================================="""

if __name__ == "__main__":
    # stats_all_repeating(50)
    # stats_all_repeating(15)
    # play_all_repeating(100000, plot = True)
    # single_player_repeating("Isaac", 500, "Place 4", 50)
    # multi_players_repeating()
    max_single_bet('2', 25)
