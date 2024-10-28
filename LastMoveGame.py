def create_board(size,symbol1,symbol2):
    board = [0]*size
    for i in range(size):
        board[i] = [0]*size
    board[0][size//2] = symbol1
    board[size-1][size//2] = symbol2
    symbol1_location = [0,size//2]
    symbol2_location = [size-1,size//2]
    
    return board,symbol1_location,symbol2_location

def print_board(current_board,columns_list):
    print("   ",end='')
    for column in range(len(current_board)):
        print(f"   {columns_list[column]}  ",end='')
    for row_index in range(len(current_board)):
        print('\n    '+('-'*5+' ')*(len(current_board)))
        print(f' {row_index+1} ',end='')
        for column_index in range(len(current_board)):
            if current_board[row_index][column_index] == 0:
                print(" |   |",end='')
            else:
                print(f" | {current_board[row_index][column_index]} |",end='')
        print(f' {row_index+1} ',end='')
    print('\n    '+('-'*5+' ')*(len(current_board)))
    print("   ",end='')
    for column in range(len(current_board)):
        print(f"   {columns_list[column]}  ",end='')
    print('\n')


def take_symbol1():
    symbol1 = input('Enter the letter to represent player 1 (except O): ').upper()
    while symbol1 == 'O':
        symbol1 = input('Enter letter other than "O": ').upper()
    return symbol1

def take_symbol2(symbol1):
    symbol2 = input('Enter the letter to represent player 2 (except O and player1 symbol): ').upper()
    while symbol2 in ['O',symbol1]:
        if symbol2 == 'O':
            symbol2 = input('Enter letter other than "O": ').upper()
        else: 
            symbol2 = input("Enter a letter other than player1: ").upper()
    return symbol2

def take_board_size():
    board_size = int(input('Enter the row/column number of the playing field (3, 5, 7): '))
    while board_size not in [3,5,7]:
        board_size = input('Enter the row/column number of the playing field (3, 5, 7): ')
    return board_size

#To get users the direction they want to go
def take_big_stone_movement_code(current_board,movement_dict,stone_location):
    print("      N    \n  NW  |  NE\n    \\ | /  \nW-----O-----E\n    / | \\  \n  SW  |  SE\n      S    ") #compass for user
    is_movement_proper = False
    while not is_movement_proper:
        movement = input().upper()
        is_movement_proper = True 
        if movement in movement_dict:

            #To check where the stone wants to go, the desired location is determined.
            location_to_check_row = stone_location[0]+movement_dict[movement][0]
            location_to_check_column = stone_location[1]+movement_dict[movement][1]

            #To check if the desired location is in the list
            try:
                current_board[location_to_check_row][location_to_check_column]
            except IndexError:
                is_movement_proper = False
                print('Move within the game limit')

            #To ensure that the stone does not move to the other side of the board.
            if is_movement_proper and (location_to_check_row < 0 or location_to_check_column < 0):
                is_movement_proper = False
                print('Move within the game limit')

            #To check if the location is filled    
            elif is_movement_proper and current_board[location_to_check_row][location_to_check_column] != 0:
                is_movement_proper = False
                print('This position is filled')
        else:
            is_movement_proper = False
    
    return movement
                
def move_big_stone(current_board,stone_location,movement_dict,movement,stone_symbol):
    current_board[stone_location[0]][stone_location[1]] = 0 #Vacates the stone's former position
    
    #The value corresponding to the desired direction is added to the position of the stone.
    stone_location[0] += movement_dict[movement][0]
    stone_location[1] += movement_dict[movement][1]

    current_board[stone_location[0]][stone_location[1]] = stone_symbol

#To get from the user the location where they want to place the small stone.
def take_small_stone_coordinates_will_place(current_board,columns_dict):
    is_coordinates_proper = False
    while not is_coordinates_proper:
        is_coordinates_proper =True
        coordinates_will_be_placed_stone = input('Enter the coordinates where you want to place the small stone(1A,2B etc): ').upper()
        if len(coordinates_will_be_placed_stone) == 2:

            #To ensure row and column are entered in the desired order
            try:
                row = int(coordinates_will_be_placed_stone[0])
            except ValueError:
                is_coordinates_proper = False
                print('row coordinate not integer')
            column = coordinates_will_be_placed_stone[1]

            #To check whether the column is entered in the desired range or not
            if is_coordinates_proper and not(column in columns_dict):
                is_coordinates_proper = False
                print('column not true')

            #To check whether the row is entered in the desired range or not
            elif is_coordinates_proper and row > len(current_board):
                is_coordinates_proper = False
                print('row coordinate out of range')
            
            #To check if the location is filled
            elif is_coordinates_proper and current_board[row-1][columns_dict[column]] != 0:
                is_coordinates_proper =False
                print('this coordinate filled')
        else:
            is_coordinates_proper = False
            print('enter 2 character')
    return row,column                                             
        
def place_small_stone(current_board,columns_dict,row,column):
    
    current_board[row-1][columns_dict[column]] = 'O'

#To check whether the big stone can move or not
def controll_big_stone_mobility(current_board,stone_location):
    can_move = False
    row = -1
    while not can_move and row <=1 : #To check from left to right of the stone
        column = -1
        while not can_move and column <=1: #To check from the top to the bottom of the stone          
            location_to_check_row = stone_location[0]+row
            location_to_check_column = stone_location[1]+column
            
            #To check if the place to check is on the other side of the list
            if location_to_check_row>=0 or location_to_check_column>=0: 
                #To check if the location to be checked is in the list
                try:
                    can_move = current_board[location_to_check_row][location_to_check_column] == 0 #if the locaiton is filled can move will be false
                except IndexError:
                    can_move = False
            else:
                can_move = False
            column += 1
        row += 1

    return can_move
            

def main():
    big_stone_movemet_dict = {'N':[-1,0],'S':[1,0],'E':[0,1],'W':[0,-1],'NE':[-1,1],'NW':[-1,-1],'SE':[1,1],'SW':[1,-1]} #Values that must be added to the position in order for the stone to move in the desired direction
    column_names = ['A','B','C','D','E','F','G']
    
    #Takes players symbol
    player1_symbol = take_symbol1()
    player2_symbol = take_symbol2(player1_symbol)

    want_to_play_again = "Y"
    while want_to_play_again == "Y":
        board_size = take_board_size()
        
        columns_dict = {}
        for i in range(board_size):  #It adds letters as large as the size of the board from the column list to the columns_dict and assigns indexes corresponding to these letters.
            columns_dict[column_names[i]] = i

        current_board,player1_location,player2_location = create_board(board_size,player1_symbol,player2_symbol) #Creates board
        
        can_move_player1 = True
        can_move_player2 = True

        print_board(current_board,column_names)
        
        while can_move_player1 and can_move_player2:
            
            #takes player 1 big stone movement and moves the stone
            print(player1_symbol, "please enter the direction you want to move your own big stone (N, S, E, W, NE, NW, SE, SW): ")
            player1_big_stone_movement = take_big_stone_movement_code(current_board,big_stone_movemet_dict,player1_location)
            move_big_stone(current_board,player1_location,big_stone_movemet_dict,player1_big_stone_movement,player1_symbol)

            print_board(current_board,column_names)

            #takes player 1 small stone placement and  places the small stone
            player1_small_stone_placement_row,player1_small_stone_placement_column =take_small_stone_coordinates_will_place(current_board,columns_dict)
            place_small_stone(current_board,columns_dict,player1_small_stone_placement_row,player1_small_stone_placement_column)
            
            print_board(current_board,column_names)

            #checks the big stones can move or not
            can_move_player1 = controll_big_stone_mobility(current_board,player1_location)
            can_move_player2 = controll_big_stone_mobility(current_board,player2_location)

            if can_move_player1 and can_move_player2:   

                #takes player 2 big stone movement and moves the stone 
                print(player2_symbol, "please enter the direction you want to move your own big stone (N, S, E, W, NE, NW, SE, SW): ")        
                player2_big_stone_movement = take_big_stone_movement_code(current_board,big_stone_movemet_dict,player2_location)
                move_big_stone(current_board,player2_location,big_stone_movemet_dict,player2_big_stone_movement,player2_symbol)

                print_board(current_board,column_names)

                #takes player 2 small stone placement and  places the small stone
                player2_small_stone_placement_row,player2_small_stone_placement_column =take_small_stone_coordinates_will_place(current_board,columns_dict)
                place_small_stone(current_board,columns_dict,player2_small_stone_placement_row,player2_small_stone_placement_column)
                
                print_board(current_board,column_names)

                #checks the big stones can move or not
                can_move_player1 = controll_big_stone_mobility(current_board,player1_location)
                can_move_player2 = controll_big_stone_mobility(current_board,player2_location)

        
        if can_move_player1: #prints the winner
            print('Player', player1_symbol ,'won the game.')
        elif can_move_player2:
            print('Player', player2_symbol ,'won the game.')
        else :
            print("The game ended in a draw")

        want_to_play_again = input('Would you like to play again(Y/N)?: ').upper()
    
    
            
main()