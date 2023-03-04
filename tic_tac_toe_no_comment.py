# Example tic_tac_toe game for Code Camp class of 2023 at LMAX.
# Makes use of functions, loops, arrays, and a light introduction to object-oriented programming.

import numpy as np

class game:
  
    def __init__(self):
        
        self.game_over = False
        
        self.board = np.zeros((3,3))
        
        self.player_dict = {1:'X',4:'O',0:'-'}
        
        self.coord_dict = {
            'a':0,'b':1,'c':2, 
            '1':0,'2':1,'3':2 
        }
    
    def play(self):
        
        self.display_board()
        
        player_turns = np.empty((9,))
        player_turns[::2] = 1
        player_turns[1::2] = 4
        
        while self.game_over == False:
            
            for player in player_turns:

                self.check_draw()
                if self.game_over == True:
                    break

                self.player_move(player)
                self.display_board()
                
                for x in self.checklist():
                    self.check_win_per_line(player,x)
                if self.game_over == True:
                    break
    
    def checklist(self):
        
        checklist = []
        
        for i in range(3):
            checklist.append(self.board[i,:])
            checklist.append(self.board[:,i])
        
        checklist.append(np.diag(self.board))
        checklist.append(np.diag(np.flip(self.board,axis=1)))

        return(checklist)
    
    def check_draw(
        self
    ):
        if (self.board!=0).all():
            print('-- Draw! --')
            self.game_over = True
    
    def check_win_per_line(
        self, 
        player, 
        x
    ):
        win_str = f'-- Player {self.player_dict[player]} wins! --'

        if x.sum() == 3*player:
            print(win_str)
            self.game_over = True
    
    def translate_coordinates(
        self,
        coord
    ):
        row = self.coord_dict[coord[0]]
        col = self.coord_dict[coord[1]]
        return(row,col)
    
    def player_move(
        self, 
        player
    ):
        player_str = self.player_dict[player]
        coord = input(f"Player {player_str}: ").lower()
            
        try:
            row, col = self.translate_coordinates(coord)
            if (self.board[row,col]!=0):
                print('Cheater!')
                self.player_move(player)
            else:
                self.board[row, col] = player
        except:
            print(f"Please input co-ordinates correctly, player {player_str}")
            self.player_move(player)
                     
    def display_board(self):
        
        print()
        display_board = np.empty((4,4), dtype = object)
        display_board[0,:]=[' ','1','2','3']
        display_board[1:,0] = ['A','B','C']
        display_board[1:,1:] = np.vectorize(
            self.player_dict.get
        )(
            self.board
        )
        print(display_board)
