# Example tic_tac_toe game for Code Camp class of 2023 at LMAX.
# Makes use of functions, loops, arrays, and a light introduction to object-oriented programming.


# we'll be using numpy as it has some handy functions that work well with arrays/matrices
import numpy as np

# the game class contains all the functions we'll need to run the game
class game:
    
    def __init__(self):
        
        """
        - This section sets all the important settings and variables for the game to run.
        - It *initialises* or instantiates the class, so to speak.
        - (Don't worry too much about this part).
        
        - The reason we do this is because we're going to use functions over and over, 
            and we want to track the important objects like the board or whether the game is over,
            by putting 'self.' before them.
        - It also lets us call on important objects many times without replicating them in our code.
            ==> laziness = good
        """
        
        # this will trigger the end of the game when set to True
        self.game_over = False
        
        # make a 3x3 board full of zeros
        self.board = np.zeros((3,3))
        
        # a dictionary translates 1=X and 4=O
        # this will help when displaying the board and printing to screen
        self.player_dict = {1:'X',4:'O',0:'-'}
        
        # this will translate user inputs into coordinates, ie A3 = (0,2)
        self.coord_dict = {
            'a':0,'b':1,'c':2, # rows
            '1':0,'2':1,'3':2  # columns
        }
        
    def checklist(self):
        """
        Returns a list of each row and column, as well as the diagonals.
        This way we can easily check whether a player has won.
        """
        
        # empty list to add, or append, the rows/cols/diags to
        checklist = []
        # rows
        for i in range(3):
            checklist.append(self.board[i,:])
        # columns
        for j in range(3):
            checklist.append(self.board[:,j])
        # diagonals
        checklist.append(np.diag(self.board))
        checklist.append(np.diag(np.flip(self.board,axis=1)))

        return(checklist)
    
    def check_draw(
        self
    ):
        """
        Checks if any of the squares are still 0. If so, the game is over.
        """
        if (self.board!=0).all():
            print('-- Draw! --')
            self.game_over = True
    
    def check_win_per_line(
        self, 
        player, 
        x
    ):
        """
        Checks whether the sum in a row/col/diag add up to 3 or 12 (X or O).
        If so, the corresponding player wins and the game is over.
        """
        win_str = f'-- Player {self.player_dict[player]} wins! --'

        if x.sum() == 3*player:
            print(win_str)
            self.game_over = True
    
    def translate_coordinates(
        self,
        coord
    ):
        """
        Translates between 'A3' and (0,2) for example.
        """
        row = self.coord_dict[coord[0]]
        col = self.coord_dict[coord[1]]
        return(row,col)
    
    def player_move(
        self, 
        player
    ):
        """
        Asks player for an input move. 
        If the space is already taken, accuses the player of cheating and tries again.
        If not correct format, will try again with a sarcastic remark.
        """
        player_str = self.player_dict[player]
        coord = input(f"Player {player_str}: ").lower()
            
        try:
            row, col = self.translate_coordinates(coord)
            if (self.board[row,col]!=0):
                print('Cheater!')
                self.player_move(player)
                # this is what's known as a 'recursion', meaning the function references itself!
            else:
                self.board[row, col] = player
        except:
            print(f"Please input co-ordinates correctly, player {player_str}")
            self.player_move(player)
    
    def play(self):
        """
        Loops through each player, and each time:
            1. Checks for a draw
            2. Asks for player move
            3. Checks for a win.
        """
        
        self.display_board()
        
        # this is just a list that alternates between X and O 9 times
        # [X,O,X,O,...]
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
                     
    def display_board(self):
        """
        Displays the game board in a disgusting way.
        """
        print()
        # empty board
        display_board = np.empty((4,4), dtype = object)
        # fill with coordinate labels
        display_board[0,:]=[' ','1','2','3']
        display_board[1:,0] = ['A','B','C']
        # update with actual board
        #     - basically we're converting the board from 1,4 to X,O using the player dictionary
        #     - google 'map numpy entries to dictionary values'
        display_board[1:,1:] = np.vectorize(
            self.player_dict.get
        )(
            self.board
        )
        print(display_board)
