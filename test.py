from confour import *

if __name__ == "__main__":
    b = Board()
    b.print_board()
    #print "segments (0,3): " + str(b.get_segments(0,3))
    #print "segments (0,6): " + str(b.get_segments(0,6))
    print "segments (3,3): " + str(b.get_segments(3,3))
