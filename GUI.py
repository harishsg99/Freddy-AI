# Chess Graphical User Interface (GUI)
# Written by Rutuparn Pawar <InputBlackBoxOutput>

import tkinter
from tkinter import *
import tkinter.messagebox as msgbox

import chess
import bot
import time

import os
import sys
#-------------------------------------------------------------------------------------------
# Unicode for chess pieces
# white king	  ♔   U+2654
# white queen	  ♕   U+2655
# white rook	  ♖   U+2656
# white bishop    ♗   U+2657
# white knight    ♘   U+2658
# white pawn	  ♙   U+2659
# black king	  ♚   U+265A
# black queen	  ♛   U+265B
# black rook	  ♜   U+265C
# black bishop    ♝   U+265D
# black knight    ♞   U+265E
# black pawn	  ♟   U+265F

unicode_map = { "K": "\u2654",
				"Q": "\u2655",
				"R": "\u2656",
				"B": "\u2657",
				"N": "\u2658",
				"P": "\u2659",

				"k": "\u265A",
				"q": "\u265B",
				"r": "\u265C",
				"b": "\u265D",
				"n": "\u265E",
				"p": "\u265F",

				"-":" "
			  }
#----------------------------------------------------------------------------------
class GUI(Tk):
	def __init__(self, width, height):
		super().__init__()

		self.title("Chess")
		self.geometry(f"{width}x{height}") 
		self.wm_resizable(width=False, height=False)

		self.board = chess.Board()
		self.moveStr = ""

		self.gameOver = False

	#-------------------------------------------------------------------------------
	# Menu bar
	def newGame(self):
		self.board = chess.Board()
		self.updateBoard(self.board)

	def about(self):
		try:
			with open(os.path.join(sys.path[0], "about.txt"), "r") as about_file:
				msgbox.showinfo('About', about_file.read())
		except FileNotFoundError:
			self.status.configure(text="File about.txt not found!")

	def createMenuBar(self):
		self.menu = Menu(self)
		self.menu.add_command(label='New game', command=self.newGame)
		self.menu.add_command(label='About', command=self.about)
		self.menu.add_command(label='Close', command=self.quit)

		self.config(menu=self.menu)

	#-------------------------------------------------------------------------------
	# Status bar
	def createStatusBar(self):
		self.status = Label(self, text="Developed by InputBlackBoxOutput", font='calibri 12 normal', borderwidth=1, relief=SUNKEN, anchor='s', pady=4)
		self.status.pack(side=BOTTOM, fill=X)

		Label(window).pack(side=BOTTOM) # Spacer

	#-------------------------------------------------------------------------------
	def updateBoard(self, board):
		boardState = ""

		for x in str(self.board.fen).split("'")[1].split(" ")[0]:
			if x.isnumeric():
				for n in range(0, int(x)):
					boardState += "-"
			else:
				if x != "/":
					boardState += x

		#print(boardState)

		for i in range(64):
				self.b_list[i].configure(text= unicode_map[boardState[i]])

	def onButtonClick(self, button):
		self.status.configure(text = "")

		if self.gameOver == False:
			# Get row
			if button >=0 and button <=31:
				if button >=0 and button <=7:
					r = 8
				if button >=8 and button <=15:
					r = 7
				if button >=16 and button <=23:
					r = 6
				if button >=24 and button <=31:
					r = 5
			else:
				if button >=32 and button <=39:
					r = 4
				if button >=40 and button <=47:
					r = 3
				if button >=48 and button <=55:
					r = 2
				if button >=56 and button <=63:
					r = 1	

			# Get column
			c = chr(97 + button%8)
			
			if len(self.moveStr) == 2:		
				try:
					self.moveStr += c + str(r)
					print(self.moveStr)

					move = chess.Move.from_uci(str(self.moveStr))
					self.moveStr = ""
					if move in self.board.legal_moves :
						self.board.push(move)
						self.updateBoard(self.board)

						time.sleep(0.1)
						bot_move = bot.minimaxRoot(3, self.board, True)
						bot_move = chess.Move.from_uci(str(bot_move))
						self.board.push(bot_move)
						self.updateBoard(self.board)
					else:
						self.status.configure(text="Illegal move")

				except ValueError:
					self.status.configure(text = "Invalid move")
					self.moveStr = ""
				

				if self.board.is_stalemate():
					self.status.configure(text = "Game Over: Stalemate")
					self.gameOver = True
				if self.board.is_insufficient_material():
					self.status.configure(text = "Game Over: Insufficient Pieces")
					self.gameOver = True
				if self.board.is_game_over():
					self.status.configure(text = "Game Over: Checkmate")
					self.gameOver = True
					
				if self.board.is_check():
					self.status.configure(text = "Check")

			else:
				self.moveStr += c + str(r)

	def createChessBoard(self, font, w, h):
		self.grid_map = Frame(window, bg='#AFAFAF', padx=1, pady=1)

		# Generate 64 button widgets
		self.b_list = []
		for each in range(0, 64):
			self.b_list.append( Button(self.grid_map, text=' ', command=lambda each=each:self.onButtonClick(each), font=f"consolas {font} normal", width=w, height=h))

		# Place 64 button widgets in a 8x8 grid
		each = 0
		for r in range(0, 8):
			for c in range(0, 8):
				self.b_list[each].grid(row=r, column=c)

				if r%2 != 0:
					if each%2 == 0:
						self.b_list[each].configure(bg='#CFCFCF')
				else:
					if each%2 != 0:
						self.b_list[each].configure(bg='#CFCFCF')
				each = each + 1

		self.grid_map.pack(side=BOTTOM)
		self.updateBoard(self.board)
#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
	window = GUI(740, 680)
	window.createMenuBar()
	window.createStatusBar()
	window.createChessBoard(18, 6, 2)
	window.mainloop()

#-------------------------------------------------------------------------------------------
# EOF