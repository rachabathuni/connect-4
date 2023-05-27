import connect4


def test_moves(moves):
    board = connect4.Board()
    board.forward(moves)
    board.print_board()

    eng = connect4.Connect4Engine(board)
    err, move = eng.get_best_move()
    if err != connect4.SUCCESS:
        print("failed to get best move")
        return
    ret = board.play(move)
    if ret != connect4.SUCCESS:
        print("Failed to make move")
        return
    board.print_board()


def test01():
    moves = [1, 0, 2, 3, 4, 5, 6, 6, 4, 5, 3, 2, 1, 1, 2, 1, 6, 3, 2, 5, 5]
    test_moves(moves)


def test03():
    moves = [3, 0, 0, 4, 5, 0, 2, 0, 3, 3, 4, 4, 4, 6, 1]
    test_moves(moves)


def test02():
    moves = [0, 6, 0, 5, 0, 4]
    test_moves(moves)


test02()
