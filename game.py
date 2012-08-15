from confour import Board, get_move

def get_human_move(board):
    board.print_board()
    col = input('Enter a column to drop your piece into, between 0 and %d: ' % (board.width - 1))
    if col not in range(board.width): raise Exception
    board.place_in_column(col)

def get_ai_move(board):
    move = get_move(b)
    b.place_in_column(move[1])
    print move
    print 'My move has a score of %d' % move[0]
    print


if __name__ == "__main__":
    b = Board()

    human = input('Type 1 to go first, 2 to go second: ')
    if human not in [1,2]: raise Exception

    if human == 1: get_human_move(b)

    while not b.ended != 0:
        get_ai_move(b)
        if b.ended > 0: break
        #b.print_board()
        get_human_move(b)

    print 'Thank you for playing! Player %d wins.' % b.ended
    b.print_board()
