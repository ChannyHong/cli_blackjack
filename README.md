# cli_blackjack

<h1>Command Line Interface Blackjack</h1>


**Description:**

- simple blackjack game
- single player against dealer and only 'stand'/'hit' options for the player

Instructions: 
With Python 2.7 installed in your command line interface, simply run the following script:

```
python blackjack.py
```

Then simply follow the prompt to play the game!


**Design Choices:**
- For the deck of cards, I simply had a list of cards (each represented by a string i.e. 'AD' is Ace of Diamonds while '5S' is the 5 of Spades). 
- At the beginning of round, the deck is shuffled using Python's random.shuffle function then cards were dealt to the player and the dealer by using the list.pop function.
- The major components of the game are (each implemented as a separate class): game, deck, dealer, and player.
- At relevant stop-points of the game, a simplistic form of the various statuses of the game is printed out (including dealer's hands, player's hands, values of hands, amount bet, player balance, etc.).
- For the 'hidden' card, the [hidden] token was used upon display.