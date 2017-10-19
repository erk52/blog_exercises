# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:18:41 2017

@author: EKish
"""

import numpy as np
from collections import defaultdict
import random


            
def half():
    return 0.5

global X_table, O_table
X_table = defaultdict(half)
O_table = defaultdict(half)

explore_default = 0.3

def make_move(board_state, t=0):
    '''Looks at current board state, chooses a move either by exploration 
    or by using the appropriate table
    '''    
    explore_prob = explore_default*np.exp(-t / 5000)
    possible_moves = np.where(board_state == 0)[0]
    
    if sum(board_state) == 0:
        my_table = X_table
        my_marker = 1
    else:
        my_table = O_table
        my_marker = -1
    
    if explore_prob > random.uniform(0,1):
        choice = random.choice(possible_moves)
    else:
        moves, scores = [], []
        for i in possible_moves:
            new_state = board_state.copy()
            new_state[i] = my_marker
            moves.append(i)
            scores.append(my_table[tuple(new_state)])
        try: move_choices = [moves[i] for i in range(len(moves)) if scores[i] == max(scores)]
        except: print(moves, scores, possible_moves)
        choice = random.choice(move_choices)
    return choice
    
def check_win(bs):
    '''Checks to see if board state has a winner
    Reurns 1 for X win, -1 for O win, 0 otherwise'''
    #Check rows
    if (sum(bs[:3]) == 3) or (sum(bs[3:6]) == 3) or (sum(bs[6:]) == 3):
        return 1
    elif (sum(bs[:3]) == -3) or (sum(bs[3:6]) == -3) or (sum(bs[6:]) == -3):
        return -1
    #check columns
    if (sum(bs[::3]) == 3) or (sum(bs[1::3]) == 3) or (sum(bs[2::3]) == 3):
        return 1
    elif (sum(bs[::3]) == -3) or (sum(bs[1::3]) == -3) or (sum(bs[2::3]) == -3):
        return -1
    #Check Diagonals
    d1 = bs[0] + bs[4] + bs[8]
    d2 = bs[2] + bs[4] + bs[6]
    if d1 == 3 or d2 == 3:
        return 1
    elif d1 == -3 or d2 == -3:
        return -1
    
    return 0
    
def run_game(t):
    '''Plays the X table against the Y table.  Uses time t to adjust
    exploration probability as the game goes on'''
    states = []
    winner = False
    alpha = 0.9
    board = np.zeros(9)
    tied = False
    while not winner:
        #X player makes move, update board
        X = make_move(board,t)
        board[X] = 1
        states.append(tuple(board))
        winner = check_win(board)
        #Break if win or tie
        if winner:
            break
            
        if 0 not in board:
            tied = True
            break
        #O player makes move, update board
        O = make_move(board,t)
        board[O] = -1
        states.append(tuple(board))
        winner = check_win(board)
        if 0 not in board:
            tied = True
            break
            
    #Make sure we played enough turns to have a full game
    table = {1: X_table, -1: O_table}
    assert len(states) > 4, "Too few states for valid game"
    
    #Winners get 1 point, losers get 0
    if not tied:
        cur_player = int(winner)
        table[cur_player][states[-1]] = 1
        table[-cur_player][states[-2]] = 0
    #Tie score gets 0.75 points
    if tied:
        if sum(board) > 0:
            cur_player = 1
        else: cur_player = -1
        table[cur_player][states[-1]] = 0.75
        table[-cur_player][states[-2]] = 0.75
    k = len(states) - 3
    while k >= 0:
        cur_state = states[k]
        next_state = states[k+2]
        table[cur_player][cur_state] = table[cur_player][cur_state] + alpha *(table[cur_player][next_state] - table[cur_player][cur_state])
        cur_player = -cur_player
        k -= 1
    
    return winner, board
    
def train_players(numsteps=20000):
    for k in range(numsteps):
        run_game(k)
        
def play_game(PLAY_AS='X'):
    new_game = np.zeros(9)
    mapping = {1.0: 'X', -1.0: 'O', 0.0 : ' '}
    while 0 in new_game or not check_win(new_game):
        if PLAY_AS == 'X':        
            for i in [0,3,6]:
                print (mapping[new_game[i]], ' | ', mapping[new_game[i+1]], ' | ', mapping[new_game[i+2]])
        
        if PLAY_AS == 'O':
            x = make_move(new_game,999999999)
        else:
            x = input('Make x move:')
            
        new_game[x] = 1
        if 0 not in new_game:
            break
        elif check_win(new_game):
            break
            
        if PLAY_AS == 'O':        
            for i in [0,3,6]:
                print (mapping[new_game[i]], ' | ', mapping[new_game[i+1]], ' | ', mapping[new_game[i+2]])
        
        if PLAY_AS == 'X':
            o = make_move(new_game,999999999)
        else:
            o = input('Make o move: ')
        new_game[o] = -1
    w = check_win(new_game)
    for i in [0,3,6]:
        print (mapping[new_game[i]], ' | ', mapping[new_game[i+1]], ' | ', mapping[new_game[i+2]])
    if w == 0:
        print('Tie game!')
    elif w == 1:
        print('X wins!')
    else:
        print('O wins!')
        
if __name__ == '__main__':
    print('Training AI players...')
    train_players(10000)
    ex_flag = False
    while not ex_flag:
        print('Play a game?  Enter X to play as X, O to play as O, or Q to quit')
        piece = input('Play as: ').upper()
        if piece not in 'XO':
            ex_flag = True
        else:
            play_game(piece)
    print('Goodbye!')
        