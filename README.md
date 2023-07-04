# Terminal Blackjack
#### Video Demo: https://youtu.be/3xONFakneAI
#### Description:

My final project for CS50P is a **Blackjack** game that can be played in the terminal window!
The project is contained entirely in project.py, and writting fully in Python. I used a little
bit of object-oriented programming to help with this game, and the rest of the game I just
made using conditionals, loops, and some good old logic.

At the top of the code, I declared some information that is of use later on in the code. I
declared a list of all the valid suits in a card deck, a list of all the valid number cards
in a card deck, and a list of all the face cards in a card deck.


Now that that is out of the way, I'll first start off my walking you through the 3 classes I defined
for the project, which are as follows:
- Card
- Player
- Balance

The class names themselves leave nothing up to the imagination, but they do have a few features
that are important. The Card class is used to instantiate every card in the deck of cards. To make
a Card, the arguments it takes is a number, and a suit, which I have a default value of None. The
str method of the Card will return a string which says the number/face and suit of the card. The eq
method is used to compare the Cards solely by value, and the hash method is used since I need to use
the Cards as keys in a dictionary later on.

The Player class has 2 properties, which are a list called cards (containing Cards), and a score.
The str method returns a format string with all the Cards in the cards list. The 2 defined properties
simply return their values. The tally method iterates through the Cards in the cards list and tallies
the score of all the cards. Aces can count as 1 or 11, the other face cards count as 10, and the
numbers count as their respectie numbers. The tally method uses these values to calculate the score
of a Player.

The Balance class has 1 instance variable, cash, which has a default value of 1000. The str method
will return a format string which puts the cash into a dollars format. The cash setter makes sure
that the cash is above 0, or else a ValueError is raised.

I defined 5 functions that I used in the code, which are:

- generate_deck
- generate_values
- add_cards
- print_score
- winner

The generate_deck function does not take any inputs, and returns a list of every card in a standard
deck of cards, where each card is a Card object. It uses a loop for each suit, and makes all the
number cards and face cards in the deck.

The generate_values function takes the Cards list from the previous function to make a dictionary,
whose keys are the Cards from the previous function, and the values are the values of each Card.
Any number Card has a value which is the number itself, the King, Queen, and Jack all have value 10,
and Aces have a value of 11.

The add_cards function takes a copy of the dictionary from the previous function, a Player, an n
number of cards to add, and the actual dictionary from the previous function. The function has no
output. The function randomly samples an n number of Cards from a list of keys of the copy
dictionary, adds them to the Player's cards list, and then removes them from the copy dictionary.
Then the score of the Player is adjusted using the Player's tally method.

The print_score function is pretty simple, it just takes a Player object as an argument, and
prints a formatted string of their score, using their score instance variable.

The winner function is the biggest function, but it's just a series of condititionals. It takes
a lot of arguments, 4 of which are boolean variables indicating whether or not the player
or dealer has a blackjack or a bust. It also takes the dealer's and player's scores, the balance,
and the bet. It will return a format of string telling the user who has won, and will adjust the
user's balance accordingly.

Now time for the main function, first, we make a balance variable which is an object of the Balance
class. Then we use the generate_deck and generate_values functions to make a deck and assign the
values of all the Cards. The shuffle function from the random library is used to shuffle all
the Cards in the deck, so that the game can be played with randomness. Then the user's balance
is printed to the display. Now time for the main game loop. The first thing in this loop, is well,
another loop. This loop simply asks the user for an integer amount for their bet, and will keep
reprompting until the user gives a valid input. Then, we initialize 4 boolean variables all to
False, these just demonstrate that neither the player or dealer have blackjack, or have busted.
Now a copy of the deck dictionary is made, so that we can remove cards from it at will. Then,
we make a player and dealer object, both of the Player class. The dealer then uses the add_cards
function to put a card into their cards list, the dealer's card is then printed, along with their
score in the terminal. The same thing is done with the player, except they get 2 cards and their
score printed in the terminal. Then the player_loop is entered, which asks the user if they would
like to get more cards to get a value closer to 21 with the risk of going over 21, or if they would
like the stand and face off with the dealer's card value. After the player wants to stand, this loop
is broken out of and the dealer_loop is entered. This loop will keep executing until the dealer's
card value is 17 or greater, when it will break and stop taking more cards. Now the player's cards
and score are printed, along with the dealer's cards and score. Using the winner function, the winner
of the game is printed using all the info, such as scores, whether anyone has busted, or whether
anyone has blackjack. If the player wins with blackjack, they get 1.5 times their bet back, if
they win by score, they get 1 times their bet back, and if they tie with score or blackjack with
the dealer, they just regain their initial bet. Otherwise, they lose their initial bet altogether.
After the game ends, the user is reprompted if they want to play again, only if their balance is
more than 0. If they choose to play again, the main game loop is executed again, but if they
don't want to, or if they have 0 money in the balance, they are met with an exit message.

That is my game! Thanks for reading!