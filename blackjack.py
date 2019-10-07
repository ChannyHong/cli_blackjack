
import random
import time




'''
Cards are defined as the following:

Ranks: 
Ace -> 'A'
Number -> n (i.e. '1')
Face -> 'J', 'Q', 'K'

Suits:
Diamonds -> 'D'
Clubs/Clover -> 'C'
Hearts -> 'H'
Spade -> 'S'

A card is a string concatenation of both i.e.:
Ace of Diamonds -> 'AD'
5 of Hearts -> '5H'
Queen of Spades -> 'QS'

'''



class Deck:
	def __init__(self):
		self.cards = None
		self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K']
		self.suits = ['D', 'C', 'H', 'S']
		
	def shuffle(self):
		self.cards = []
		for rank in self.ranks:
			for suit in self.suits:
				self.cards.append(rank+suit)
		random.shuffle(self.cards)

class Dealer:
	def __init__(self):
		self.value = 0
		self.hidden_card = None
		self.hand = []
		self.in_play = True
		self.ace_count = 0

class Game:
	def __init__(self, deck, dealer, player):
		self.bet_amount = 0
		self.deck = deck
		self.dealer = dealer
		self.player = player
		self.pushed = False

	def reset(self, bet_pushed=False):
		if not bet_pushed:
			self.bet_amount = 0

		self.deck.shuffle()

		self.dealer.value = 0
		self.dealer.hidden_card = None
		self.dealer.hand = []
		self.dealer.in_play = True
		self.dealer.ace_count = 0

		self.player.value = 0
		self.player.hand = []
		self.player.keep_acting = True
		self.player.in_play = True
		self.player.has_blackjack = False
		self.player.ace_count = 0

class Player:
	def __init__(self, name, starting_cash):
		self.name = name
		self.balance = starting_cash
		self.keep_playing = True
		self.keep_acting = True
		self.in_play = True
		self.hand = []
		self.value = 0
		self.has_blackjack = False
		self.ace_count = 0







def get_card_value(card):
	rank = card[0]
	value = None

	number_ranks_set = set(['2', '3', '4', '5', '6', '7', '8', '9'])
	face_ranks_set = set(['J', 'Q', 'K'])

	if rank == 'A':
		value = 11

	elif rank in number_ranks_set:
		value = int(rank)

	elif rank in face_ranks_set:
		value = 10

	else:
		print("Something went terribly wrong")

	return value



def print_game_state(game, dealer, player):
	time.sleep(2) # for dramatic card reveal

	print("\n\n\n#############################")

	print("The bet amount of the current round is: ${}".format(game.bet_amount))

	print("\n")

	if dealer.hidden_card == None:
		print("Dealer's cards are:")
	else:
		print("Dealer's cards are:\n[hidden]")
	for card in dealer.hand:
		print(card)
	print("Dealer's value is {}".format(dealer.value))

	print("\n")

	print("{}'s cards are:".format(player.name))
	for card in player.hand:
		print(card)
	print("{}'s value is {}".format(player.name, player.value))

	print("\n")

	print("{}'s balance is ${}".format(player.name, player.balance))

	print("#############################\n\n\n")


def play_blackjack():

	#######################################
	############# Game Setup #############
	#######################################
	print("Welcome to Blackjack (21) : Command Line Interface!")

	player_name = raw_input("Please enter your name: ")
	print("Welcome, {}!".format(player_name))

	print("How much cash would you like to start with, {}?".format(player_name))
	starting_cash = int(raw_input("Enter cash amount: $"))

	# initialize each component of blackjack
	player = Player(player_name, starting_cash)
	deck = Deck()
	dealer = Dealer()
	game = Game(deck, dealer, player)
	





	#######################################
	############# Play Rounds #############
	#######################################
	while player.keep_playing:

		############# Shuffle Cards #############
		print("Shuffling cards...")
		deck.shuffle()

		############# Place Wager #############
		print("{}'s balance is: ${}".format(player.name, player.balance))
		bet_amount = int(raw_input("Please enter {}'s bet: $".format(player.name)))
		game.bet_amount += bet_amount
		player.balance -= bet_amount

		############# Deal Cards #############
		print("Dealing cards...")
		# First time dealt
		for recipient in [player, dealer]:
			next_card = deck.cards.pop()
			if next_card[0] == 'A':
				recipient.ace_count += 1

			if recipient is dealer:
				recipient.hidden_card = next_card
			else:
				recipient.hand.append(next_card)
				recipient.value += get_card_value(next_card)

		raw_input("Press any key for first cards...")
		print_game_state(game, dealer, player)

		# Second time dealt
		for recipient in [player, dealer]:
			next_card = deck.cards.pop()
			if next_card[0] == 'A':
				recipient.ace_count += 1
			recipient.hand.append(next_card)
			recipient.value += get_card_value(next_card)

		raw_input("Press any key for second cards...")
		print_game_state(game, dealer, player)

		# Corner case of 2 aces from the get-go
		if player.value > 21:
			if player.ace_count > 0:
				player.value -= 10
				player.ace_count -= 1

	
		###########################################
		############# Player's Action #############
		###########################################
		while player.keep_acting and player.in_play:

			############# Check If Blackjack #############
			if player.value == 21:
				print("You have a blackjack!")
				player.has_blackjack = True

				print("Revealing dealer's hidden card...")
				# reveal hidden card
				dealer.hand.append(dealer.hidden_card)
				dealer.value += get_card_value(dealer.hidden_card)
				dealer.hidden_card = None

				print_game_state(game, dealer, player)

				if player.value > dealer.value:
					print("Since the dealer does not have a blackjack, {} won!".format(player.name))
					player.balance += game.bet_amount + game.bet_amount

				elif player.value == dealer.value:
					print("The dealer also has a blackjack! We have a tie and so the previous bet amount is pushed to the next round.")
					game.pushed = True
				
				break

			############# Execute Player Action #############
			player.intent = raw_input("What would you like to do?\n(stand / hit): ")

			if player.intent == "stand":
				player.keep_acting = False

			elif player.intent == "hit":
				next_card = deck.cards.pop()
				if next_card[0] == 'A':
					player.ace_count += 1
				player.hand.append(next_card)
				player.value += get_card_value(next_card)

				

				# Check if busted
				if player.value > 21:
					if player.ace_count > 0:
						player.value -= 10
						player.ace_count -= 1
						print_game_state(game, dealer, player)
					else:
						print_game_state(game, dealer, player)
						player.in_play = False
						print("{} is busted!".format(player.name))

				else:
					print_game_state(game, dealer, player)
					

			elif player.intent == "double_down":
				print("Not yet implemented")

			elif player.intent == "split":
				print("Not yet implemented")

			elif player.intent == "surrender":
				print("Not yet implemented")

			else:
				print("Something went terribly wrong")



		if not player.has_blackjack:

			############# Dealer's Action #############
			if player.in_play:

				# reveal hidden card
				dealer.hand.append(dealer.hidden_card)
				dealer.value += get_card_value(dealer.hidden_card)
				dealer.hidden_card = None

				print_game_state(game, dealer, player)

				while dealer.value < 17:
					next_card = deck.cards.pop()
					if next_card[0] == 'A':
						recipient.ace_count += 1
					dealer.hand.append(next_card)
					dealer.value += get_card_value(next_card)

					print_game_state(game, dealer, player)

					# Check if busted
					if dealer.value > 21:
						if dealer.ace_count > 0:
							dealer.value -= 10
							dealer.ace_count -= 1
						else:
							dealer.in_play = False
							print("Dealer is busted!")


			############# Decide Winner #############
			if not player.in_play:
				print("Dealer wins since {} is busted!".format(player.name))

			elif not dealer.in_play:
				print("{} wins since dealer is busted!".format(player.name))
				player.balance += game.bet_amount + game.bet_amount

			elif player.in_play and dealer.in_play:
				if player.value < dealer.value:
					print("Dealer wins since dealer's hand is higher than {}'s!".format(player.name))

				elif player.value > dealer.value:
					print("{} wins since {}'s hand is higher than dealer's!".format(player.name, player.name))
					player.balance += game.bet_amount + game.bet_amount

				elif player.value == dealer.value:
					print("We have a tie! The previous bet amount is pushed to the next round.")
					game.reset(bet_pushed = True)
					game.pushed = True

		
		############# Ask Player If Keep Playing #############
		if not game.pushed:
			keep_playing = int(raw_input("Would you like to keep playing?\n(1 for yes / 2 for no): "))
			if keep_playing == 1:
				game.reset(bet_pushed = False)
				#print_game_state(game, dealer, player)

			if keep_playing == 2:
				player.keep_playing = False
				print("Thanks for playing Blackjack! Goodbye.")

		elif game.pushed:
			game.reset(bet_pushed = True)
			game.pushed = False




if __name__ == "__main__":
	play_blackjack()





