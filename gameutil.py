# Functions for the game
def checkmuhle(ringPos, stellePos, spielfeld, spielfeld_muhlen, mancolor):
    if stellePos%2 == 0:  # Men on the edge
        if spielfeld[ringPos][(stellePos+1)%8] == mancolor and spielfeld[ringPos][(stellePos+2)%8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos + 1) % 8] = 1  # Set mill in projection
            spielfeld_muhlen[ringPos][(stellePos + 2) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
        if spielfeld[ringPos][(stellePos-1)%8] == mancolor and spielfeld[ringPos][(stellePos-2)%8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos - 1) % 8] = 1  # Set mill in projection
            spielfeld_muhlen[ringPos][(stellePos - 2) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
    else:  # Men in the centre lines
        if spielfeld[(ringPos+1)%3][stellePos] == mancolor and spielfeld[(ringPos+2)%3][stellePos] == mancolor:
            spielfeld_muhlen[(ringPos + 1) % 3][stellePos] = 1  # Set mill in projection
            spielfeld_muhlen[(ringPos + 2) % 3][stellePos] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
        if spielfeld[ringPos][(stellePos + 1) % 8] == mancolor and spielfeld[ringPos][(stellePos - 1) % 8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos + 1) % 8] = 1
            spielfeld_muhlen[ringPos][(stellePos - 1) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
    return False

# TODO: Test clearmuhlen, DOESNT WORK
def clearmuhlen(spielfeld, spielfeld_muhlen):  # Clear out any destroyed mills from the projection matrix
    tobecleared = []
    for ring_pos in range(len(spielfeld)):
        for stelle_pos in range(len(spielfeld[ring_pos])):
            temp_team = spielfeld[ring_pos][stelle_pos]
            if temp_team == 0:
                tobecleared.append((ring_pos, stelle_pos))
            elif stelle_pos % 2 == 0:  # Edge case
                if (spielfeld[ring_pos][(stelle_pos+1) % 8] != temp_team or spielfeld[ring_pos][(stelle_pos+2) % 8] != temp_team) and \
                        (spielfeld[ring_pos][(stelle_pos-1) % 8] != temp_team or spielfeld[ring_pos][(stelle_pos-2) % 8] != temp_team):
                    tobecleared.append((ring_pos, stelle_pos))
            else:  # Center case
                if (spielfeld[(ring_pos+1)%3][stelle_pos] != temp_team or spielfeld[(ring_pos+2)%3][stelle_pos] != temp_team) and \
                        (spielfeld[ring_pos][(stelle_pos+1)%8] != temp_team or spielfeld[ring_pos][(stelle_pos-1)%8] != temp_team):
                    tobecleared.append((ring_pos, stelle_pos))
    for clear in tobecleared:
        spielfeld_muhlen[clear[0]][clear[1]] = 0
    print(spielfeld_muhlen)

def removeman(ringpos, stellepos, spielfeld):
    myteam = 1 if turn else 2
    if spielfeld[ringpos][stellepos] == myteam or spielfeld[ringpos][stellepos] == 0 or spielfeld_muhlen[ringpos]\
            [stellepos] == 1:
        if not hasnotonlymills(1 if myteam == 2 else 2):
            spielfeld[ringpos][stellepos] = 0
            remaining[myteam] -= 1
            return True
        return False
    else:
        spielfeld[ringpos][stellepos] = 0
        remaining[myteam] -= 1
        return True


def canmove(ringpos, stellepos, spielfeld):
    if stellepos % 2 == 0:  # Men on the edges
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
    else:  # Men on the center fields
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
        if ringpos == 0:  # Outer ring
            if spielfeld[1][stellepos] == 0:
                return True
        if ringpos == 1:  # Center ring
            if spielfeld[0][stellepos] == 0 or spielfeld[2][stellepos] == 0:
                return True
        if ringpos == 2:  # Inner ring
            if spielfeld[1][stellepos] == 0:
                return True
    return False


def canjump(spielfeld):
    for reihe in spielfeld:
        for stelle in reihe:
            if stelle == 0:
                return True
    return False


def checkremaining(player):
    if remaining[player] < 3:
        return True
    return False


def canmoveatall(player, spielfeld):
    for ring in range(len(spielfeld)):
        for stelle in range(len(spielfeld[ring])):
            if spielfeld[ring][stelle] == player:
                if canmove(ring, stelle, spielfeld):
                    return True
    return False


def hasnotonlymills(player, spielfeld, spielfeld_muhlen):
    for i in range(len(spielfeld_muhlen)):
        for j in range(len(spielfeld_muhlen[i])):
            if spielfeld_muhlen[i][j] == 0:
                if spielfeld[i][j] == player:
                    return True
    return False


def isneighbor(select_ring, select_stelle, origin_ring, origin_stelle):
    if ((origin_stelle + 1) % 8 == select_stelle or (origin_stelle - 1) % 8 == select_stelle) and origin_ring == select_ring:
        return True  # Left/Right
    if origin_stelle % 2 != 0:  # Center positions
        if ((origin_stelle + 1) % 8 == select_stelle or (origin_stelle - 1) % 8 == select_stelle) and origin_ring == select_ring:
            return True
        if origin_ring == 0:
            if select_ring == origin_ring + 1 and select_stelle == origin_stelle:
                return True
        if origin_ring == 1:
            if origin_ring + 1 == select_ring or origin_ring - 1 == select_ring and select_stelle == origin_stelle:
                return True
        if origin_ring == 2:
            if origin_ring - 1 == select_ring and select_stelle == origin_stelle:
                return True
    return False