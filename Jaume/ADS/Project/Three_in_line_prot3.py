import sys

class Three_in_line(object):

	def __init__(self):
		
		self.n = 3

		# Creation of a matrix n*n representing the board
		self.board = [[' ' for _ in range(self.n)] for _ in range(self.n)] 
		
		# Initializing the players
		self.player1 = ''  
		self.player2 = ''

	def represent_board(self):

		'''
		Function that allows us to visualize the board
		'''
		line = '-'*self.n + '-'*(self.n - 1) # Calculating the nº of dashes needed for each line depending on n
		print(line)

		# Iterating through each of the n rows of the board
		for row in self.board:
			
			# Representation of the board:
			print('|'.join(row))
			print(line)

		print() # Empty line as separator
			
	def is_board_full(self):

		'''
		Function that check if the board is full (no more space to put a piece)
		Output: True / False
		'''

		# Iterating throug each cell of the matrix
		for i in range(self.n):

			for j in range(self.n):

				# Cheking if there is an empty cell in the board
				if self.board[i][j] == ' ':

					return False # If so the board is not false and we return False

		return True

	def is_game_ended(self):

		'''
		Function that checks if the game has ended (to know when to finish the game)
		It does so by ckecking if the board is full or if one of the players has won
		Output: True / False
		'''

		# Cheking if one of the players have won and if the board is full or not
		return self.check_winner(self.player1) or self.check_winner(self.player2) or self.is_board_full()

	def check_winner(self, player):
		"""
		Function that takes self and the player as arguments and tells us if a determined player is the winner or not.
		Output: True / False
		"""

		# Counters for rows, columns, and diagonals
		row_counts = [0] * self.n
		col_counts = [0] * self.n
		main_diag_count = 0
		sec_diag_count = 0

		# Iterating through all the matrix
		for i in range(self.n):

			for j in range(self.n):

				# Counting player symbols in rows and columns
				if self.board[i][j] == player:
					row_counts[i] += 1
					col_counts[j] += 1

					# Updating diagonal counts by checking if the conditions for a diagonal are met
					if i == j:
						main_diag_count += 1

					if i + j == self.n - 1:
						sec_diag_count += 1

					# Checking if any row, column, or diagonal has all player symbols
					if row_counts[i] == self.n or col_counts[j] == self.n or main_diag_count == self.n or sec_diag_count == self.n:
						
						return True # If so the player has won and we return True

		return False # If the function continues until here it means that the player has not won so returning False

	def ask_move(self):

		print("Please do your move (Input example: '>>>i j')")

		move = sys.stdin.readline().strip().split() # Getting and formating input from stdin
		print() # Formatting output

		return int(move[0])-1, int(move[1])-1 # Returning the coordinates
	
	def choose_player(self):

		print('Chose your symbol: X / O')
		symb = sys.stdin.readline().strip()

		if symb == 'X':
			self.player1 = 'X'
			self.player2 = 'O'
		
		elif symb == 'O':
			self.player1 = 'O'
			self.player2 = 'X'

		else:
			print("Invalid input. Tryining again...")
			self.choose_player()

		print() # Formatting the output (empty line)


	def get_moves(self):
		'''
		Function that looks for all the possible moves for the bot
		'''

		moves = [] # Creating empty list to store all the legal moves

		# Iterating through each cell of the board matrix
		for i in range(self.n):

			for j in range(self.n):
				
				# Checking if there is an empty space
				if self.board[i][j] == ' ':
					
					moves.append((i, j)) # If there is an empty space we append it's coordinates into the moves list

		return moves
	
	def A0_star(self, possible_moves):

		'''
		Function that implements the A0 star algorithm to select the best movement
		It will decide which move of the possible moves is the best
		'''

		return possible_moves[0]
	
	def make_move(self, move, player):

		'''
		Function that modifies the board matrix to make the move

		Input: self, the move (i,j as positions) and which player will do the move
		'''

		i, j = move # Separing the variable move into the 2 indices

		self.board[i][j] = player # Modifying the pos i,j of the matrix board with the symbol of the player
	
	def play(self):
		'''
		Function that implements all the other functions so that it is possible to play
		'''
		print('Welcome to Three in a row\n')

		self.choose_player()
		
		self.represent_board() # Representing the board

		while self.is_game_ended() == False:

			m = self.ask_move() # Player moves first so we ask for it's move

			while m not in self.get_moves(): # Checking if a move is illegal

				print("Illegal move. Try again")

				m = self.ask_move() # Aking for a new move
			
			self.make_move(m, self.player1) # Doing player's move

			self.represent_board() # Representing the board

			best_move = self.A0_star(self.get_moves()) # Computing the best move for the bot

			self.make_move(best_move, self.player2) #  Making bot's move

			self.represent_board() # Representing the board

		if self.is_board_full(): # Checking if the board is full

			print('The board is full. No winners')

		elif self.check_winner(self.player1): # Checking if the player has won

			print("Congralutations, you won!")

		elif self.check_winner(self.player2): # Checking if the bot has won

			print("You lost! Better luck next time.")

		else: # Possible errors
			print("Something unexpected has occurred")

def main():

	'''
	Testing that the functions work correctly
	'''

	game = Three_in_line()

	game.represent_board()

	game.make_move((0,0), 'X')
	game.make_move((1,1), 'X')
	game.make_move((2,2), 'X')

	game.represent_board()

	print('Did "X" win?')
	a = game.check_winner('X')
	print(a)

	print('Did "O" win?')
	a = game.check_winner('O')
	print(a)

	print("\nIs the board full?")
	a = game.is_board_full()
	print(a)

	print("\nDid the game end?")
	a = game.is_game_ended()
	print(a)

	game = Three_in_line()
	game.make_move((0,0), 'X')
	game.make_move((0,1), 'O')
	game.make_move((0,2), 'X')

	game.represent_board()
	print("\nDid the game end?")
	a = game.is_game_ended()
	print(a)

	print("Filling the board...")
	game = Three_in_line()

	game.make_move((0,0), 'O')
	game.make_move((0,1), 'X')
	game.make_move((0,2), 'O')

	game.make_move((1,0), 'O')
	game.make_move((1,1), 'X')
	game.make_move((1,2), 'X')

	game.make_move((2,0), 'X')
	game.make_move((2,1), 'O')
	game.make_move((2,2), 'O')

	game.represent_board()

	print("\nIs the board full?")
	a = game.is_board_full()
	print(a)

	print('Did "X" win?')
	a = game.check_winner('X')
	print(a)

	print('Did "O" win?')
	a = game.check_winner('O')
	print(a)

	print("\nDid the game end?")
	a = game.is_game_ended()
	print(a)

	print("\n------------------------------------------------------\n")

	game = Three_in_line()

	game.play()

if __name__ == "__main__":
	
	main()