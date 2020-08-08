# Chess AI bot
# Code originally written by AnthonyASanchez
# Modified by Rutuparn Pawar <InputBlackBoxOutput>

import chess

#-----------------------------------------------------------------------------------
def minimaxRoot(depth, board,isMaximizing):
	possibleMoves = board.legal_moves
	bestMove = -9999
	bestMoveFinal = None
	for x in possibleMoves:
		move = chess.Move.from_uci(str(x))
		board.push(move)
		value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
		board.pop()
		if( value > bestMove):
			print("Best score: " ,str(bestMove))
			print("Best move: ",str(bestMoveFinal))
			bestMove = value
			bestMoveFinal = move
	return bestMoveFinal

#-----------------------------------------------------------------------------------
def minimax(depth, board, alpha, beta, is_maximizing):
	if(depth == 0):
		return -evaluation(board)
	possibleMoves = board.legal_moves
	if(is_maximizing):
		bestMove = -9999
		for x in possibleMoves:
			move = chess.Move.from_uci(str(x))
			board.push(move)
			bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
			board.pop()
			alpha = max(alpha,bestMove)
			if beta <= alpha:
				return bestMove
		return bestMove
	else:
		bestMove = 9999
		for x in possibleMoves:
			move = chess.Move.from_uci(str(x))
			board.push(move)
			bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not is_maximizing))
			board.pop()
			beta = min(beta,bestMove)
			if(beta <= alpha):
				return bestMove
		return bestMove

#-----------------------------------------------------------------------------------
def calculateMove(board):
	possible_moves = board.legal_moves
	if(len(possible_moves) == 0):
		print("No more possible moves...Game Over")
		sys.exit()
	bestMove = None
	bestValue = -9999
	n = 0
	for x in possible_moves:
		move = chess.Move.from_uci(str(x))
		board.push(move)
		boardValue = -evaluation(board)
		board.pop()
		if(boardValue > bestValue):
			bestValue = boardValue
			bestMove = move

	return bestMove

#-----------------------------------------------------------------------------------
def evaluation(board):
	i = 0
	evaluation = 0
	x = True
	try:
		x = bool(board.piece_at(i).color)
	except AttributeError as e:
		x = x
	while i < 63:
		i += 1
		evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
	return evaluation

#-----------------------------------------------------------------------------------
def getPieceValue(piece):
	if(piece == None):
		return 0
	value = 0
	if piece == "P" or piece == "p":
		value = 10
	if piece == "N" or piece == "n":
		value = 30
	if piece == "B" or piece == "b":
		value = 30
	if piece == "R" or piece == "r":
		value = 50
	if piece == "Q" or piece == "q":
		value = 90
	if piece == 'K' or piece == 'k':
		value = 900
	#value = value if (board.piece_at(place)).color else -value
	return value

#-----------------------------------------------------------------------------------
def main():
	board = chess.Board()
	n = 0
	print(board)
	while n < 200:
		usr_move = input("\nEnter move: ")
		if(len(usr_move) == 4):
			move = chess.Move.from_uci(str(usr_move))
			
			if(move in board.legal_moves):
				board.push(move)
				
				print("\nComputers Turn:")
				move = minimaxRoot(3,board,True)
				move = chess.Move.from_uci(str(move))
				board.push(move)
				print(board)
				
				if board.is_stalemate():
					print("Game Over: Stalemate")
					break
				if board.is_insufficient_material():
					print("Game Over: Insufficient Pieces")
					break
				if board.is_game_over():
					print("Game Over: Checkmate")
					break
					
				if board.is_check():
					print("Check")
			else:
				print("Illegal move")
			
		n += 1

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
	main()
	
#-----------------------------------------------------------------------------------