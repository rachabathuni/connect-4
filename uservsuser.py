import sys
import connect4


def play(board):
    board.print_board()
    while True:
        if board.is_full():
            print("No more moves")
            sys.exit(0)

        while True:
            try:
                userin = input("Enter column: ")
            except:
                return
            try:
                col = int(userin.strip())
                break
            except ValueError:
                print("Invalid entry")
                continue

        ret = board.play(col)
        if ret != connect4.SUCCESS:
            print("Failed to make move")
            return
        ret = board.check_win()
        board.print_board()
        if ret:
            print(f"Player {connect4.PLAYER_TEXT[board.get_last_player()]} won!")
            return


board = connect4.Board()
if len(sys.argv) > 1:
    movestr = sys.argv[1]
    strmoves = movestr.split(', ')
    moves = []
    for c in strmoves:
        moves.append(int(c))
    board.forward(moves)
play(board)
print("\nMove stack:")
print(board.move_stack)


