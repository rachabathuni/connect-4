import pkgutil

import connect4

g_file_handle = None

def play_comp(n_moves):
    board = connect4.Board()
    for i in range(n_moves):
        eng = connect4.Connect4Engine(board)
        e, m = eng.get_best_move()
        if e != connect4.SUCCESS:
            print("Failed to get best move")
            return -1, None
        e = board.play(m)
        if e != connect4.SUCCESS:
            print("Failed to play move")
            return -1, None
        if board.check_win():
            board.undo()
            return i-1, board

    return n_moves, board


def get_min_bucket(recs):
    m = recs[0]
    min_bucket = 0
    for i in range(len(recs)):
        if recs[i] < m:
            m = recs[i]
            min_bucket = i
    return min_bucket


def check_max_records_reached(recs, max_records_per_bucket):
    for i in recs:
        if i < max_records_per_bucket:
            return False
    return True


def save_record(nmvs, board, nextmv):
    global g_file_handle
    if not g_file_handle:
        g_file_handle = open("out.txt", "w")
    g_file_handle.write(f"{nmvs}, ")
    for r in range(board.rows):
        for c in range(board.columns):
            g_file_handle.write(f"{board.board[r][c]}, ")
    g_file_handle.write(f"{nextmv}")
    g_file_handle.write("\n")
    g_file_handle.flush()


max_records = 100000
max_records_per_position = int(max_records/42)
records = [0] * max_records_per_position

while True:
    m = get_min_bucket(records)
    n_moves, b = play_comp(m)
    eng = connect4.Connect4Engine(b)
    err, next_move = eng.get_best_move()
    if err != connect4.SUCCESS:
        print("Failed to get best move")
        continue
    save_record(n_moves, b, next_move)
    records[n_moves] += 1
    if check_max_records_reached(records, max_records_per_position):
        break
    print(records)
