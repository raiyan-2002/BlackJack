import random

# declare all card suits, number cards, and face cards
#iasdasdasd

suits = ["Hearts", "Diamonds", "Spades", "Clubs"]

num_cards = [i for i in range(2, 11)]

face_cards = ["Jack", "Queen", "King", "Ace"]


# define a Card class which takes a num, and suit argument
class Card:
    def __init__(self, num, suit=None):
        self.num = str(num)
        self.suit = suit

    # this is what i want to appear when printing the cards
    def __str__(self):
        return "{num} of {suit}".format(num = self.num, suit = self.suit)

    # use this to compare Cards
    def __eq__(self, other):
        return self.num == other.num

    # need hash for using as dict keys
    def __hash__(self):
        return hash((self.num, self.suit))


# define a Player class, which contains the players cards and current score
class Player:
    def __init__(self, cards=[], score=0):
        self._cards = cards
        self._score = score

    def __str__(self):
        start = "Cards: "
        for card in self._cards:
            start += str(card) + ", "
        return start[:-2]

    @property
    def score(self):
        return self._score

    @property
    def cards(self):
        return self._cards

    # this method will tally the score of a Player, using the deck dictionary
    def tally(self, deck):
        total = 0
        for i, card in enumerate(self._cards):
            if card.num == "Ace":
                if Card("Ace") in self._cards[:i]:
                    total += 1
                else:
                    total += deck[card]
            else:
                total += deck[card]
        if Card("Ace") in self._cards and total > 21:
            total -= 10
        self._score = total


# define a Balance class, which contains the current balance of the player, also checking if their cash is more than 0
class Balance:
    def __init__(self, cash=1000):
        self.cash = cash

    def __str__(self):
        return "Balance: ${cash}".format(cash = round((self.cash), 2))

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        if cash >= 0:
            self._cash = cash
        else:
            raise ValueError


# this will generate a list of all the decks
def generate_deck():
    cards = []
    for i in suits:
        for k, card in enumerate(num_cards):
            cards.append(Card(num_cards[k], i))
        for card in face_cards:
            cards.append(Card(card, i))
    return cards


# this will generate a dict of all the Cards in the deck and their respective values
def generate_values(cards):
    deck = {}
    for card in cards:
        if card.num in ["King", "Queen", "Jack"]:
            deck[card] = 10
        elif card.num == "Ace":
            deck[card] = 11
        else:
            deck[card] = int(card.num)
    return deck


# this function will add Cards to a Player objects cards list
def add_cards(copy, player, num, deck):
    new = random.sample(list(copy.keys()), num)
    for i in new:
        del copy[i]
    length = len(player._cards)
    if length == 0:
        player._cards = new
    else:
        player._cards.extend(new)
    player.tally(deck)


# this function will print the score of an inputted Player
def print_score(player):
    print("Score: {score}\n".format(score = player._score))


# this function will return the text to print after the game ends, and will adjust balance.cash accordingly
def winner(
    player_win,
    dealer_win,
    player_bust,
    dealer_bust,
    player_score,
    dealer_score,
    balance,
    bet,
):
    if player_win or dealer_win:  # if either player or dealer got blackjack
        if (
            dealer_win and player_win
        ):  # if both players have blackjack, it is a tie, reimburse money
            balance.cash += bet
            return "Tie!\n"

        elif player_win:
            balance.cash += 2.5 * bet
            return "You win!\n"

        else:
            return "Dealer wins!\n"

    elif dealer_bust or player_bust:  # if either player or dealer busted
        if (
            dealer_bust and player_bust
        ):  # if dealer busts but not the player player wins
            return "You both lose!\n"
        elif (
            player_bust and not dealer_bust
        ):  # if player busts but not the dealer, dealer wins
            return "Dealer wins!\n"
        else:
            balance.cash += 2 * bet
            return "You win!\n"

    else:  # if neither player or dealer won or bust
        if player_score > dealer_score:
            balance.cash += 2 * bet
            return "You win!\n"

        elif player_score < dealer_score:
            return "Dealer wins!\n"
        else:
            balance.cash += bet
            return "Tie!\n"


def main():
    # assign the balance of the player, default value is 1000
    balance = Balance()

    # generate a list of Card objects, shuffle them, and then make a dict with each Card as a key and its value
    cards = generate_deck()
    random.shuffle(cards)
    deck = generate_values(cards)

    # print the user's balance
    print("{balance} \n".format(balance = str(balance)))

    while True:
        # get the user's bet amount
        while True:
            try:
                bet = int(input("How much would you like to bet? $"))
                balance.cash -= bet
                print("\n")
                break
            except ValueError:
                pass

        
        # these boolean variables will represent if the dealer of the player have won yet
        player_win = False
        dealer_win = False

        # these boolean variables will represent whether or not the player or dealer has busted
        player_bust = False
        dealer_bust = False

        # make a copy of the cards dict so that we can remove stuff from it
        copy = deck.copy()

        # this boolean variables will allow us to run the player loop
        player_loop = True

        # make a player and a dealer using the Player class
        player = Player()
        dealer = Player()

        # get the dealer's first Card, and say that they have a hidden card
        add_cards(copy, dealer, 1, deck)
        print("DEALER")
        print(str(dealer) + " and a hidden card")
        print_score(dealer)

        # get the second card of the dealer, and add it to their list
        add_cards(copy, dealer, 1, deck)

        # get the player's first two cards, print them along with their score
        add_cards(copy, player, 2, deck)
        print("PLAYER")
        print(player)
        print_score(player)

        # if these 2 cards get a score of 21, that means the player has already won, print blackjack
        if player._score == 21:
            print("You have Blackjack!\n")
            player_loop = False
            player_win = True

        # this is the player loop, it will keep executing if the user wants to hit
        # the loop will end if the user wants to stand, or if they get blackjack, or if they bust
        while player_loop:
            while True:
                response = input(
                    "Would you like to hit or stand? (h for hit, s for stand) "
                )
                print("\n")

                # if user wants to hit, put another card in their card list, and delete the card from the copy deck
                if response == "h":
                    add_cards(copy, player, 1, deck)
                    break

                # if the player wants to stand, end the loop
                elif response == "s":
                    player_loop = False
                    break
                pass

            # print the players cards and score after every time they hit or stand
            print("PLAYER")
            print(player)
            print_score(player)

            # if the score is over 21, the player busts, and their loop ends
            if player._score > 21:
                print("You Bust!\n")
                player_loop = False
                player_bust = True

            # if the player gets 21, the player wins, and their loop ends
            elif player._score == 21:
                print("You have Blackjack!\n")
                player_loop = False
                player_win = True

        # this is the automatic dealer loop
        while dealer._score <= 16:
            add_cards(copy, dealer, 1, deck)

        print("DEALER")
        print(dealer)
        print_score(dealer)

        # if the score is over 21, the player busts, and their loop ends
        if dealer._score > 21:
            print("Dealer Busts!\n")
            dealer_bust = True

        # if the player gets 21, the player wins, and their loop ends
        elif dealer._score == 21:
            print("Dealer has Blackjack!\n")
            dealer_win = True

        print(
            winner(
                player_win,
                dealer_win,
                player_bust,
                dealer_bust,
                player._score,
                dealer._score,
                balance,
                bet,
            )
        )

        print("{balance}\n".format(balance=balance))

        # ask if user wants to play again, but only if they have enough money
        if balance.cash > 0:
            replay = input(
                "Would you like to play again? (y for yes, any other key for no) "
            )
            print("\n")
            if replay == "y":
                continue
            else:
                break
        else:
            break

    # if they don't play again, give them this exit message
    print("You left with ${balance}. Thanks for playing!".format(balance = str(balance.cash)))


if __name__ == "__main__":
    main()
