#whenever you go to a place, call the function to see where you can go now
    #terminal condition when you repeate squares
    #first recursion one move, second 2 moves

def solveable(p_idxs, k_idx):
    """Returns True (false) if all pawn locations can be capture by sequential knight moves"""
    # 1) Base case - is the puzzle solved?
    if len(p_idxs) == 0:
        #if no pawns left, return True, puzzle solved
        return True
    # 2) Find all valid_moves
    av_moves = []
    k_moves = valid_moves(k_idx)
    for p in p_idxs:
        if p in k_moves:
            #trying all knight moves to see if they take a pawn
            #storring available pawn moves into av_moves
            av_moves.append(p) 
                
    # 3) Try all valid_moves
    for a in av_moves:
        #trying all moves to see if they solve the puzzle
        p_idxs.remove(a)
        if solveable(p_idxs, a):
            return True
        else:
            #if taking that pawn didn't work, put it back, try a new move
            p_idxs.add(a)

    # 4) If nothing worked in step 3, there's no solution with the knight in this position
    return False


def valid_moves(k_idx):
    """Returns set of all valid moves from k_idx, assuming an 8x8 chess board"""
    #knight moves diagonally 2 and 1
    #first check if the move is on the board, then append if it is
    myset = set()
    #up 2 right 1
    if((k_idx[0]+2)<8 and (k_idx[1]+1)<8):
        myset.add((k_idx[0]+2, k_idx[1]+1))
    #up 2 left 1
    if((k_idx[0]+2)<8 and (k_idx[1]-1)>-1):
        myset.add((k_idx[0]+2, k_idx[1]-1))
    #down two right 1
    if((k_idx[0]-2)>-1 and (k_idx[1]+1)<8):
        myset.add((k_idx[0]-2, k_idx[1]+1))
    #down two left 1
    if((k_idx[0]-2)>-1 and (k_idx[1]-1)>-1):
        myset.add((k_idx[0]-2, k_idx[1]-1))
    #up 1 right 2
    if((k_idx[0]+1)<8 and (k_idx[1]+2)<8):
        myset.add((k_idx[0]+1, k_idx[1]+2))
    #up 1 left 2
    if((k_idx[0]+1)<8 and (k_idx[1]-2)>-1):
        myset.add((k_idx[0]+1, k_idx[1]-2))
    #down 1 right 2
    if((k_idx[0]-1)>-1 and (k_idx[1]+2)<8):
        myset.add((k_idx[0]-1, k_idx[1]+2))
    #down 1 left 2
    if((k_idx[0]-1)>-1 and (k_idx[1]-2)>-1):
        myset.add((k_idx[0]-1, k_idx[1]-2))
    return myset

    