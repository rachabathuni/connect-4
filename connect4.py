import sys
import random
import copy

N_COLUMNS = 7
N_ROWS = 6
TO_WIN = 4

BLANK = 0
PLAYER_1 = 1
PLAYER_2 = 2 
PLAYER_TEXT = ["-", "O", "X"]
PLAYER_TEXT_HIGHLIGHT = ["-", "\033[91mO\033[0m", "\033[91mX\033[0m"]
PLAYER_TEXT_STREAM = ["-", "o", "x"]
PLAYER_TEXT_HIGHLIGHT_STREAM = ["-", "O", "X"]

SUCCESS = 0
ERR_COLUMN_FULL = 1
ERR_INVALID_ROW = 2
ERR_INVALID_COLUMN = 3
ERR_STACK_EMPTY = 4
ERR_NO_MOVES_ALLOWED = 5


MAX_DEPTH = TO_WIN + 3
MIN_WEIGHT = -100000

DEBUG = False


def debug(msg):
    if DEBUG:
        sys.stderr.write(msg)
        sys.stderr.write("\n")


class Board:
    def __init__(self):
        self.columns = N_COLUMNS
        self.towin = TO_WIN
        self.rows = N_ROWS
        self.board = []
        self.chips_in_column = [0] * self.columns
        self.move_stack = []
        for i in range(self.rows):
            self.board.append([BLANK] * self.columns)
        self.positive_diag = []
        for i in range(self.rows):
            self.positive_diag.append([None] * self.columns)
        self.negative_diag = []
        for i in range(self.rows):
            self.negative_diag.append([None] * self.columns)
        self._calculate_diags()
        self.next_player = PLAYER_1

    def _calculate_diags(self):
        # Positive
        for i in range(self.columns):
            points = []
            cr = 0
            for j in range(0, min(self.columns-i, self.rows)):
                points.append([cr, i+j])
                cr += 1
            if len(points) >= self.towin:
                for point in points:
                    self.positive_diag[point[0]][point[1]] = points

        for i in range(self.rows):
            points = []
            cc = 0
            for j in range(0, min([self.rows-i, self.columns])):
                points.append([i+j, cc])
                cc += 1
            if len(points) >= self.towin:
                for point in points:
                    self.positive_diag[point[0]][point[1]] = points

        # Negative
        for i in range(self.columns):
            points = []
            cr = 0
            for j in range(0, min([i, self.rows])):
                points.append([cr, i-j])
                cr += 1
            if len(points) >= self.towin:
                for point in points:
                    self.negative_diag[point[0]][point[1]] = points

        for i in range(self.rows):
            points = []
            cc = self.columns-1
            for j in range(0, min([self.rows-i, self.columns])):
                points.append([i+j, cc])
                cc -= 1
            if len(points) >= self.towin:
                for point in points:
                    self.negative_diag[point[0]][point[1]] = points

    def get_columns(self):
        return self.columns

    def get_rows(self):
        return self.rows

    def play(self, column):
        if self.columns <= column:
            return ERR_INVALID_COLUMN

        if self.chips_in_column[column] == self.rows:
            return ERR_COLUMN_FULL

        self.board[self.chips_in_column[column]][column] = self.next_player
        self.chips_in_column[column] += 1
        self.move_stack.append(column)
        self._flip_player()
        return SUCCESS

    def undo(self):
        if len(self.move_stack) == 0:
            return ERR_STACK_EMPTY

        column = self.move_stack.pop(-1)
        self.board[self.chips_in_column[column]-1][column] = BLANK
        self.chips_in_column[column] -= 1
        self._flip_player()
        return SUCCESS

    def _check_column_win(self, player, column):
        return self._check_column_seq(player, column, self.towin)

    def _check_column_seq(self, player, column, target_seq):
        if self.chips_in_column[column] < self.towin:
            return False

        seq = 0
        for i in range(self.chips_in_column[column]):
            if self.board[i][column] == player:
                seq += 1
                if seq == target_seq:
                    return True
            else:
                seq = 0
        return False

    def _check_row_win(self, player, column):
        return self._check_row_seq(player, column, self.towin)

    def _check_row_seq(self, player, column, target_seq):
        seq = 0
        row = self.chips_in_column[column] - 1
        for c in range(self.columns):
            if self.board[row][c] == player:
                seq += 1
                if seq == target_seq:
                    return True
            else:
                seq = 0
        return False

    def _check_one_diag(self, player, diag, row, column, target_seq):
        if diag[row][column]:
            seq = 0
            for point in diag[row][column]:
                if self.board[point[0]][point[1]] == player:
                    seq += 1
                    if seq == target_seq:
                        return True
                else:
                    seq = 0
        return False

    def _check_diag_win(self, player, column):
        return self._check_diag_seq(player, column, self.towin)

    def _check_diag_seq(self, player, column, target_seq):
        row = self.chips_in_column[column]-1
        if self._check_one_diag(player, self.positive_diag, row, column, target_seq):
            return True
        if self._check_one_diag(player, self.negative_diag, row, column, target_seq):
            return True
        return False

    def _flip_player(self):
        self.next_player = PLAYER_2 if self.next_player == PLAYER_1 else PLAYER_1

    def get_last_player(self):
        return PLAYER_2 if self.next_player == PLAYER_1 else PLAYER_1

    def check_win(self):
        player = self.get_last_player()
        column = self.move_stack[-1]
        if self._check_column_win(player, column):
            return True

        if self._check_row_win(player, column):
            return True

        if self._check_diag_win(player, column):
            return True

        return False

    def check_win_in_one(self):
        player = self.get_last_player()
        column = self.move_stack[-1]
        if self._check_column_seq(player, column, self.towin-1):
            return True

        if self._check_row_seq(player, column, self.towin-1):
            return True

        if self._check_diag_seq(player, column, self.towin-1):
            return True

        return False

    def get_chips_in_column(self, column):
        return self.chips_in_column[column]

    def is_column_full(self, column):
        return self.chips_in_column[column] == self.rows

    def is_full(self):
        for c in self.chips_in_column:
            if c < self.rows:
                return False
        return True

    def forward(self, moves):
        ret = None
        for m in moves:
            ret = self.play(m)
            if ret != SUCCESS:
                return ret
            ret = self.check_win()
            if ret:
                ret = ERR_NO_MOVES_ALLOWED
                break
        return ret

    def print_board(self, outstream=sys.stdout):
        last_move = None
        if self.move_stack:
            last_move = [self.chips_in_column[self.move_stack[-1]]-1, self.move_stack[-1]]
        if not DEBUG and outstream == sys.stderr:
            return

        if outstream == sys.stderr:
            player_text_default = PLAYER_TEXT_STREAM
            player_text_highlight = PLAYER_TEXT_HIGHLIGHT_STREAM
        else:
            player_text_default = PLAYER_TEXT
            player_text_highlight = PLAYER_TEXT_HIGHLIGHT

        for r in range(self.rows-1, -1, -1):
            for c in range(len(self.board[r])):
                player_text = player_text_default
                if last_move and \
                        r == last_move[0] and c == last_move[1] and \
                        outstream != sys.stderr:
                    player_text = player_text_highlight
                outstream.write(f"{player_text[self.board[r][c]]} ")
            outstream.write("\n")
        for i in range(self.columns):
            outstream.write(f"{i} ")
        outstream.write("\n")
        outstream.write("======================\n")


class Connect4Engine:
    def __init__(self, board):
        self.board = board
        self.iter_count = 0

    def _get_max_possible_depth(self, remaining_iters, moves):
        columns = self.board.columns
        for i in range(1, 100):
            if moves ** i > remaining_iters:
                return i-1
        return 100


    def _get_weight(self, board: Board, column: int,
                    depth: int, max_depth: int, player_multiplier: int) -> int:
        player = board.next_player
        ret = board.play(column)
        if ret != SUCCESS:
            return 0

        weight = self._get_position_weight(board, depth, max_depth, player_multiplier)

        board.undo()
        return weight

    def _get_position_weight(self, board, depth, max_depth, player_multiplier):
        ret = board.check_win()
        self.iter_count += 1
        if ret:
            weight = (max_depth - depth + 1) 
            return weight

        if depth == max_depth:
            return 0

        moves = []
        for i in range(board.columns):
            if not board.is_column_full(i):
                moves.append(self._get_weight(board, i, depth+1,max_depth, 1))

        if len(moves) == 0:
            return 0

        return max(moves) * (-1) * player_multiplier

    def _find_best_move(self, board, max_depth):
        next_moves = [x for x in range(0, board.columns)]
        remaining_iters = (board.columns ** MAX_DEPTH) * 2
        cur_depth = 0
        while True:
            cur_depth += 1
            max_possible_depth = self._get_max_possible_depth(remaining_iters, len(next_moves))
            # print(f"cur_depth: {cur_depth}, max_pos_depth: {max_possible_depth}")
            if cur_depth > max_possible_depth:
                break

            moves = []
            self.iter_count = 0
            for i in range(len(next_moves)):
                if not board.is_column_full(next_moves[i]):
                    moves.append([next_moves[i], self._get_weight(board, next_moves[i], 1, cur_depth, 1)])
            remaining_iters -= self.iter_count
            print(f"fbm moves: {moves}, cur_depth: {cur_depth}")

            if len(moves) == 0:
                # This should never happen. This means board is full.
                return None

            short_list = []
            m = (-1 * cur_depth) - 1
            for i in range(len(moves)):
                if moves[i][1] > m:
                    short_list = [moves[i][0]]
                    m = moves[i][1]
                elif moves[i][1] == m:
                    short_list.append(moves[i][0])
            print(f"fbm next_moves: {short_list}")
            if len(short_list) == 1:
                return short_list[0]
            elif m != 0:
                # If we already have weights for all moves, going deeper won't change the result
                break
            next_moves = short_list

        return next_moves[random.randint(0, len(next_moves)-1)]

    def get_best_move(self):
        column = self._find_best_move(self.board, MAX_DEPTH)
        return column


