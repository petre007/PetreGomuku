from copy import deepcopy
import random

def printBoard(board):
    """
    This function is used to print the state of the board
    in which the game take place.

    @param board
    """
    board_string = " |a|b|c|d|e|f|g|h|\n" + "+-+-+-+-+-+-+-+-+-\n"
    for i in range(8):
        board_string = board_string + str(i+1)+"|" + ("|".join(str(var) for var in board[i]) + "|\n").replace("0", " ").replace(
            "1", "X").replace("2", "O")
    board_string = board_string + "+-+-+-+-+-+-+-+-+-\n"
    print(board_string)


def posToIndex(s):
    """
    This function is used to convert the literal coordinates into
    matrix indices.

    @param s
    @return r, c
    """
    s = s.lower().replace(" ", "")
    c = int(ord(s[0]) - 97)
    r = int(s[1]) - 1
    return r, c


def indexToPosition(t):
    """
    This function is used to convert matrix indices into literal
    coordinates.

    @param t
    @return pos
    """
    r = t[0] + 1
    c = chr(int(t[1]) + 97)
    pos = str(c) + str(r)
    return pos


def loadgame(filename):
    """
    This function is used to load data from a game that took place
    into our environment

    @param filename
    @return game
    """
    with open(filename) as file:
        text_file = file.readlines()
        player1 = text_file[0].replace("\n", "")
        player2 = text_file[1].replace("\n", "")
        who = text_file[2].replace("\n", "")
        board = []
        for i in range(3, 11):
            board.append(text_file[i].replace("\n", "").split(","))
        game_load = {
            "player1": player1,
            "player2": player2,
            "who": who,
            "board": board,
        }
        return game_load


def getValidMoves(board):
    """
    This function analyse the game and return every possible
    move that can be done in the game as matrix indices

    @param board
    @return possible_moves
    """
    possible_moves = []
    for i in range(8):
        for j in range(8):
            if int(board[i][j]) == 0:
                possible_moves.append((i, j))
    return possible_moves


def makeMove(board, make, who):
    """
    This function is used to position an element on the
    board, on a valid place.

    @param board
    @param who
    @param make
    """
    board[make[0]][make[1]] = who


def hasWon(board, who):
    """
    This function check if player that is assigned with "who" have won
    the game by checking if his position is the one that get him this status.

    @param board
    @param who
    @return boolean
    """
    # rows
    for i in range(8):
        for j in range(4):
            if int(board[i][j]) == who and int(board[i][j + 1]) == who and int(board[i][j + 2]) == who and int(
                    board[i][j + 3]) == who and int(board[i][j + 4]) == who:
                return True
    # col
    for i in range(4):
        for j in range(8):
            if int(board[i][j]) == who and int(board[i + 1][j]) == who and int(board[i + 2][j]) == who and int(
                    board[i + 3][j]) == who and int(board[i + 4][j]) == who:
                return True
    # diag principal
    aux = 0
    while aux < 4:
        for i in range(4):
            try:
                if (int(board[i][i + aux]) == who and int(board[i + 1][i + aux + 1]) == who and int(
                        board[i + 2][i + aux + 2]) == who and int(board[i + 3][i + aux + 3]) == who and int(
                        board[i + 4][i + aux + 4]) == who) or (
                        int(board[i + aux][i]) == who and int(board[i + aux + 1][i + 1]) == who and int(
                        board[i + aux + 2][i + 2]) == who and int(board[i + aux + 3][i + 3]) == who and int(
                        board[i + aux + 4][i + 4]) == who):
                    return True
            except IndexError:
                continue
        aux += 1

    aux2 = 0
    while aux2 < 4:
        for i in range(4):
            if (int(board[i][7-i-aux2]) == who and int(board[i+1][7-i-1-aux2]) == who and int(board[i+2][7-i-2-aux2]) == who and int(board[i+3][7-i-3-aux2]) == who and int(board[i+4][7-i-4-aux2]) == who) or (
                    int(board[i+aux2][7 - i]) == who and int(board[i + 1+aux2][7 - i - 1]) == who and int(
                board[i + 2+aux2][7 - i - 2]) == who and int(board[i + 3+aux2][7 - i - 3]) == who and int(
                board[i + 4+aux2][7 - i - 4]) == who
            ):
                return True
        aux2 += 1
    return False


def checkMovesDoneInRowsRightToLeft(board, who, i, j):
    if j < 8:
        if int(board[i][j+1]) == who:
            return checkMovesDoneInRowsRightToLeft(board, who, i, j+1)
        else:
            return i, j

def checkMovesDoneInRowsLeftToRightToLeft(board, who, i, j):
    if j > 0:
        if int(board[i][j-1]) == who:
            return checkMovesDoneInRowsLeftToRightToLeft(board, who, i, j-1)
        else:
            return i, j

def checkMovesDoneInColumnsBottomToTop(board, who, i, j):
    if i >= 0:
        if int(board[i-1][j]) == who:
            return checkMovesDoneInColumnsBottomToTop(board, who, i-1, j)
        else:
            return i, j

def checkMovesDoneInColumnsTopToBottom(board, who, i, j):
    if i < 8:
        if int(board[i+1][j]) == who:
            return checkMovesDoneInColumnsTopToBottom(board, who, i+1, j)
        else:
            return i, j

def returnFirstWhoDetectedOnLineRightToLeft(board, who):
    for i in range(8):
        for j in range(8):
            if int(board[i][j]) == who:
                return i, j
    return None, None

def returnFirstWhoDetectedOnBottomToTop(board, who):
    for i in reversed(range(8)):
        for j in reversed(range(8)):
            if int(board[i][j]) == who:
                return i, j
    return None, None

def returnFirstWhoDetectedOnLineLeftToRight(board, who):
    for i in range(8):
        for j in reversed(range(8)):
            if int(board[i][j]) == who:
                return i, j
    return None, None

def suggestMove1(board, who):
    """
    This method analyse all the situation in which you can
    position to win.

    @param board
    @param who
    @return suggested_moves
    """
    board_copy = deepcopy(board)
    valid_moves_list = getValidMoves(board_copy)
    suggested_move_list = []
    i, j = returnFirstWhoDetectedOnLineRightToLeft(board_copy, who)
    if i is not None and j is not None:
        try:
            r_rows, c_rows = checkMovesDoneInRowsRightToLeft(board_copy, who, i, j)
            aux = 4-(c_rows - j)
            suggested_move_list_aux = []
            if aux + c_rows < 8:
                for k in range(1, aux+1):
                    if (r_rows, c_rows+k) in valid_moves_list:
                        makeMove(board_copy, (r_rows, c_rows+k), who)
                        suggested_move_list_aux.append((r_rows, c_rows+k))
                        if hasWon(board_copy, who):
                            for suggested_move in suggested_move_list_aux:
                                suggested_move_list.append(suggested_move)
                    else:
                        break
        except IndexError:
            print("No good indexes")
        except TypeError:
            print("No good indexes")
    else:
        index = random.randint(1, len(getValidMoves(board)))
        return getValidMoves(board)[index-1]
    board_copy = deepcopy(board)
    try:
        i1, j1 = returnFirstWhoDetectedOnLineLeftToRight(board_copy, who)
        r_rows1, c_rows1 = checkMovesDoneInRowsLeftToRightToLeft(board_copy, who, i1, j1)
        aux1 = 4 - (j1 - c_rows1)
        if c_rows1 - aux1 >= 0:
            suggested_move_list_aux1 = []
            for k in range(1, aux1+1):
                if (r_rows1, c_rows1 - k) in valid_moves_list:
                    makeMove(board_copy, (r_rows1, c_rows1 - k), who)
                    suggested_move_list_aux1.append((r_rows1, c_rows1 - k))
                    if hasWon(board_copy, who):
                        for suggested_move in suggested_move_list_aux1:
                            suggested_move_list.append(suggested_move)
                else:
                    break
    except IndexError:
        print("No good indexes")
    except TypeError:
        print("No good indexes")
    board_copy = deepcopy(board)
    try:
        i2, j2 = returnFirstWhoDetectedOnBottomToTop(board_copy, who)
        r_cols, c_cols = checkMovesDoneInColumnsBottomToTop(board_copy, who, i2, j2)
        aux2 = 4 - (i2 - c_cols)
        if c_cols - aux2 >= 0:
            suggested_move_list_aux2 = []
            for k in range(1, aux2+1):
                if (r_cols - k, c_cols) in valid_moves_list:
                    makeMove(board_copy, (r_cols - k, c_cols), who)
                    suggested_move_list_aux2.append((r_cols - k, c_cols))
                    if hasWon(board_copy, who):
                        for suggested_move in suggested_move_list_aux2:
                            suggested_move_list.append(suggested_move)
    except IndexError:
        print("No good indexes")
    except TypeError:
        print("No good indexes")
    board_copy = deepcopy(board)
    try:
        i3, j3 = returnFirstWhoDetectedOnLineLeftToRight(board_copy, who)
        r_cols1, c_cols1 = checkMovesDoneInColumnsTopToBottom(board_copy, who, i3, j3)
        aux3 = 4 - (r_cols1 - i3)
        if r_cols1 + aux3 < 8:
            suggested_move_list_aux3 = []
            for k in range(1, aux3+1):
                if (r_cols1 + k, c_cols) in valid_moves_list:
                    makeMove(board_copy, (r_cols1 + k, c_cols1), who)
                    suggested_move_list_aux3.append((r_cols1 + k, c_cols1))
                    if hasWon(board_copy, who):
                        for suggested_move in suggested_move_list_aux3:
                            suggested_move_list.append(suggested_move)
    except IndexError:
        print("No good indexes")
    except TypeError:
        print("No good indexes")
    if len(suggested_move_list) > 0:
        return set(suggested_move_list)
    else:
        index = random.randint(1, len(getValidMoves(board)))
        return getValidMoves(board)[index-1]


def newGame(player1, player2):
    """
    This method return a fresh new game.

    @param player1:
    @param player2:
    @return game
    """
    return {
        "player1": player1,
        "player2": player2,
        "who": 1,
        "board": [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]
    }

def play():
    """
     This is the main function which initialize the game.
    """
    print("*"*55)
    print("***" + " " * 8 + "WELCOME TO PETRE'S GOMOKU!" + " " * 8 + "***")
    print("*" * 55, "\n")
    print("Enter the players' names by typing 'P', or type 'C' to \nplay with computer or 'L' to load a game.\n")
    comand = input("Comand: ")
    if comand == 'P':
        player1_is_empty = True
        player1 = ""
        while player1_is_empty:
            player1 = input("Name of player1: ")
            if len(player1) > 1:
                player1_is_empty = False
        player2_is_empty = True
        player2 = ""
        while player2_is_empty:
            player2 = input("Name of player2: ")
            if len(player2) > 1 and player1 != player2:
                player2_is_empty = False
        game = newGame(player1, player2)
        print("\n")
        print("***" + " " * 8 + "HAVE FUN!" + " " * 8 + "***")
        print("\n")
        who = int(game["who"])
        game_on_going = True
        while game_on_going:
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 1:
                is_valid = True
                while is_valid:
                    position = posToIndex(input(player1 + " please insert your move: "))
                    if position in valid_moves:
                        is_valid = False
                    else:
                        print("Illegal position. Please insert another move.")
                makeMove(game["board"], position, who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player1+" HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 2
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 2:
                is_valid = True
                while is_valid:
                    position = posToIndex(input(player2 + " please insert your move: "))
                    if position in valid_moves:
                        is_valid = False
                    else:
                        print("Illegal position. Please insert another move.")
                makeMove(game["board"], position, who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player2+" HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 1
            if len(valid_moves) == 0 and not hasWon(game["board"], 1) and not hasWon(game["board"], 2):
                game_on_going = False
                print("The game ended in a draw")
    if comand == 'L':
        text_file = input("Enter the name of the game from files: ")
        game = loadgame(text_file)
        player1 = game["player1"]
        player2 = game["player2"]
        print("\n")
        print("***" + " " * 8 + "HAVE FUN!" + " " * 8 + "***")
        print("\n")
        who = int(game["who"])
        game_on_going = True
        while game_on_going:
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 1:
                is_valid = True
                while is_valid:
                    position = posToIndex(input(player1 + " please insert your move: "))
                    if position in valid_moves:
                        is_valid = False
                    else:
                        print("Illegal position. Please insert another move.")
                makeMove(game["board"], position, who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player1 + " HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 2
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 2:
                is_valid = True
                while is_valid:
                    position = posToIndex(input(player2 + " please insert your move: "))
                    if position in valid_moves:
                        is_valid = False
                    else:
                        print("Illegal position. Please insert another move.")
                makeMove(game["board"], position, who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player2 + " HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 1
            if len(valid_moves) == 0 and not hasWon(game["board"], 1) and not hasWon(game["board"], 2):
                game_on_going = False
                print("The game ended in a draw")
    if comand == 'C':
        player1_is_empty = True
        player1 = ""
        while player1_is_empty:
            player1 = input("Name of player1: ")
            if len(player1) > 1:
                player1_is_empty = False
        player2 = "C"
        game = newGame(player1, player2)
        print("\n")
        print("***" + " " * 8 + "HAVE FUN!" + " " * 8 + "***")
        print("\n")
        who = int(game["who"])
        game_on_going = True
        while game_on_going:
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 1:
                is_valid = True
                while is_valid:
                    position = posToIndex(input(player1 + " please insert your move: "))
                    if position in valid_moves:
                        is_valid = False
                    else:
                        print("Illegal position. Please insert another move.")
                makeMove(game["board"], position, who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player1 + " HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 2
            valid_moves = getValidMoves(game["board"])
            printBoard(game["board"])
            if who == 2:
                position = suggestMove1(game["board"], who)
                print(str(position))
                if type(position) is tuple:
                    print("In Tupla")
                    makeMove(game["board"], position, who)
                if type(position) is set:
                    print("In lista")
                    position = list(position)
                    is_valid = True
                    while is_valid:
                        position = list(position)
                        for i in range(len(position)):
                            if position[i] in valid_moves:
                                makeMove(game["board"], position[i], who)
                                is_valid = False
                                break
                            else:
                                position = suggestMove1(game["board"], who)
                if hasWon(game["board"], who):
                    print("\n")
                    print(player2 + " HAS WON THE GAME!")
                    game_on_going = False
                else:
                    who = 1
            if len(valid_moves) == 0 and not hasWon(game["board"], 1) and not hasWon(game["board"], 2):
                game_on_going = False
                print("The game ended in a draw")

play()
