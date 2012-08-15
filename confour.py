from copy import deepcopy
import heapq

DEPTH = 5
RED   = 1 # max
BLACK = 2 # min

class Board:
    def __init__(self, width=7, height=6, win_len=4):
        self.width = width
        self.height = height
        self.win_len = win_len

        self.grid = [[0] * width for i in range(height)]
        self.num_in_column = [0] * width
        self.current_player = RED
        self.last_move = -1
        self.ended = 0

        self.red_segments = []
        self.black_segments = []

    def print_board(self):
        for row in reversed(self.grid):
            for cell in row:
                print cell,
            print
        print

    def place_in_column(self, col):
        row = self.num_in_column[col]
        if row == self.height: raise IndexError
        self.grid[row][col] = self.current_player
        self.num_in_column[col] += 1
        self.last_move = col

        if self.check_win(row, col) != 0:
            self.ended = self.current_player

        self.current_player ^= 3

    def check_win(self, row, col):
        color = self.grid[row][col]
        return any([self.__num_in_direction(color, row, col, i, j) >= self.win_len for (i,j) in [(1, 0), (0, 1), (1, 1), (1, -1)]])

    def __num_in_direction(self, color, row, col, deltax, deltay):
        def inner(dx, dy):
            count = 0
            x, y = row, col
            for i in range(self.width + self.height):
                x, y = x + dx, y + dy
                try:
                    assert(x >= 0 and y >= 0)
                    if self.grid[x][y] != color: return count
                except IndexError:
                    return count
                except AssertionError:
                    return count
                count += 1
            return count
        return 1 + inner(deltax, deltay) + inner(-deltax, -deltay)

    def children(self):
        ch = []
        for i in range(self.width):
            b = deepcopy(self)
            try:
                b.place_in_column(i)
                ch.append(b)
            except IndexError:
                pass
        return ch

    def get_segments(self, row, col):
        segments = []
        rmin, cmin = max(0, row + 1 - self.win_len), max(0, col + 1 - self.win_len)
        rmax, cmax = min(self.height - self.win_len, row), min(self.width - self.win_len, col)

        # rows
        c = cmin
        while c <= cmax:
            segments.append([(row, i) for i in range(c, c + self.win_len)])
            c += 1

        # columns
        r = rmin
        while r <=rmax:
            segments.append([(i, col) for i in range(r, r + self.win_len)])
            r += 1

        # up-right diagonals
        r, c = row, col
        while r >= rmin and c >= cmin:
            seg = []
            i, j = r, c
            while i < r + self.win_len and j < c + self.win_len:
                if i in range(self.height) and j in range(self.width):
                    seg.append((i, j))
                else:
                    break
                i, j = i + 1, j + 1
            if len(seg) == self.win_len:
                segments.append(seg)
            r, c = r - 1, c - 1

        # up-left diagonals
        r, c = row, col
        while r <= rmax + self.win_len  and c >= cmin:
            seg = []
            i, j = r, c
            while i > r - self.win_len and j < c + self.win_len:
                if i in range(self.height) and j in range(self.width):
                    seg.append((i, j))
                else:
                    break
                i, j = i - 1, j + 1
            if len(seg) == self.win_len:
                segments.append(seg)
            r, c = r + 1, c - 1
        return segments

    def score(self):
        s = 0
        if self.ended == RED: return 1000
        elif self.ended == BLACK: return -1000

        for row in range(self.height):
            for col in range(self.width):
                segments = self.get_segments(row, col)
                for seg in segments:
                    num_red = sum(map(lambda x: 1 if self.grid[x[0]][x[1]] == RED else 0, seg))
                    num_black = sum(map(lambda x: 1 if self.grid[x[0]][x[1]] == BLACK else 0, seg))
                    if num_red == 0 or num_black == 0:
                        s += num_red**2
                        s -= num_black**2

        return s

    def score2(self):
        s = 0
        if self.ended == RED: return 1000
        elif self.ended == BLACK: return -1000

        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == RED:
                    t = self.__num_in_direction(RED, row, col, 1, 0)
                    s += t**2
                    t = self.__num_in_direction(RED, row, col, 1, 1)
                    s += t**2
                    t = self.__num_in_direction(RED, row, col, 0, 1)
                    s += t**2
                    t = self.__num_in_direction(RED, row, col, 1, -1)
                    s += t**2
                elif self.grid[row][col] == BLACK:
                    t = self.__num_in_direction(BLACK, row, col, 1, 0)
                    t -= t**2
                    t = self.__num_in_direction(BLACK, row, col, 1, 1)
                    t -= t**2
                    t = self.__num_in_direction(BLACK, row, col, 0, 1)
                    t -= t**2
                    t = self.__num_in_direction(BLACK, row, col, 1, -1)
                    t -= t**2

        return s

def alphabeta(board, depth, alpha, beta, player, move):
    if depth == 0 or board.ended != 0:
        return board.score(), move
    if player == RED:
        for child in reversed(board.children()):
            alpha, move = max((alpha, move), (alphabeta(child, depth-1, alpha, beta, player^3, move)[0], child.last_move))
            if beta <= alpha: break
        return alpha, move
    else:
        for child in board.children():
            beta, move = min((beta, move), (alphabeta(child, depth-1, alpha, beta, player^3, move)[0], child.last_move))
            if beta <= alpha: break
        return beta, move

def get_move(board):
    return alphabeta(board, DEPTH, -99999999, 99999999, board.current_player, -1)
    #moves = []
    #for i in range(board.width):
        #b = deepcopy(board)
        #try:
            #b.place_in_column(i)
            #moves.append((alphabeta(b, DEPTH, float('-inf'), float('inf'), b.current_player), i))
        #except IndexError, e:
            #pass
    #if board.current_player == RED:
        #return max(moves)
    #else:
        #return min(moves)
