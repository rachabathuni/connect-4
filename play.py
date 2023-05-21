import sys
import connect4

board = connect4.Board()
board.print_board()
while True:
    player = board.next_player
    if board.is_full():
        print("No more moves")
        sys.exit(0)

    while True:
        print(f"Player: {connect4.PLAYER_TEXT[player]}")
        userin = input("Enter column: ")
        try:
            col = int(userin.strip())
            break
        except ValueError:
            print("Invalid entry")
            continue
    ret = board.play(col)
    if ret != connect4.SUCCESS:
        print("Failed to make move")
        sys.exit(0)
    ret = board.check_win()
    board.print_board()
    if ret == connect4.WIN_FOUND:
        print("User won!")
        sys.exit(0)

    if board.is_full():
        print("No more moves")
        sys.exit(0)

    print("Thinking...")
    eng = connect4.Connect4Engine(board)
    move = eng.get_best_move()
    ret = board.play(move)
    if ret != connect4.SUCCESS:
        print("Failed to make move")
        sys.exit(0)
    ret = board.check_win()
    board.print_board()
    if ret == connect4.WIN_FOUND:
        print("Computer won!")
        sys.exit(0)


