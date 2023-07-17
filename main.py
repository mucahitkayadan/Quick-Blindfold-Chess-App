# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:29:54 2023

@author: muham
"""

import speech_recognition as sr
import chess
import chess.engine
import os

def recognize_speech_from_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your move...")
        audio = r.listen(source)

    try:
        move = r.recognize_google(audio)
        print("You said:", move)
        return move
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
    except sr.RequestError as e:
        print("Error:", str(e))

def make_computer_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=2.0))
    board.push(result.move)
    print("Computer's move:", result.move)

# Create a chess board and Stockfish engine
board = chess.Board()
stockfishPath = os.getcwd() + '/stockfish.exe'
engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)

while not board.is_game_over():
    # Get player's move from voice input
    player_move = recognize_speech_from_mic()

    # Validate and make the player's move
    if player_move in [str(move) for move in board.legal_moves]:
        move = chess.Move.from_uci(player_move)
        board.push(move)
        print("Your move:", move)
        make_computer_move(board, engine)
    else:
        print("Invalid move. Try again.")

    # Make the computer's move using Stockfish
    

# Game over
print("Game over. Result:", board.result())

# Close the Stockfish engine
engine.quit()
