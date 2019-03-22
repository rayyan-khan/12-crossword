import re
import sys

# crossword assignment v1 due 3/15

# inputs
input = sys.argv[1:]
print('Input:', input)

height, width, numBlocks = 0, 0, 0
wordDict = ''
hWords, vWords = [], [] # [(vPos, hPos, word), ...]

# test for matches:
# 0 indicates HxW
# 1 indicated number of blocks
# 2 indicates horizontal words
# 3 indicates vertical words
matchTests = [r'^(\d+)x(\d+)$', r'^\d+$', r'^H(\d+)x(\d+)(.+)$', r'^V(\d+)x(\d+)(.+)$']

for arg in input:
    if '.txt' in arg.lower():
        wordDict = arg
        continue
    for testNum, matchTest in enumerate(matchTests):
        match = re.search(matchTest, arg, re.I)
        if not match: continue
        if testNum == 0:
            height = int(arg[:arg.lower().find('x')])
            width = int(arg[arg.lower().find('x')+1:])
        elif testNum == 1:
            numBlocks = int(arg)
        elif testNum == 2:
            vPos, hPos, word = int(match.group(1)), int(match.group(2)),\
                               match.group(3).lower()
            hWords.append((vPos, hPos, word))
        elif testNum == 3:
            vPos, hPos, word = int(match.group(1)), int(match.group(2)), \
                               match.group(3).lower()
            vWords.append((vPos, hPos, word))

#print('Inputs: \n Dictionary: {}\n HxW = {}x{}\n numBlocks = {}\n hWords = {}\n vWords = {}'
#      .format(wordDict, height, width, numBlocks, hWords, vWords))

##################
# HELPER METHODS #


def printXW(puzzle, width):
    for index in range(len(puzzle)):  # matr is a string in this case
        if index % width == 0:  # left side
            print('{} '.format(puzzle[index]), end='')
        elif index % width == width - 1:  # right side
            print('{}\n'.format(puzzle[index]), end='')
        else:
            print('{} '.format(puzzle[index]), end='')
    print('\n')


def addVword(xw, vPos, hPos, word, width):
    wordIndexes = []
    wordList = [letter for letter in word][::-1]
    for k in range(len(word)):
        index = (vPos + k)*width + hPos
        if index > len(xw)-1:
            print('Word doesn\'t fit in location. (V)')
            return -1
        wordIndexes.append(index)
    checkIndexes = {xw[i] for i in wordIndexes}
    if checkIndexes != {'-'}:
        print('Can\'t place word over non-empty space. (V)')
        return -1
    else:
        newXW = ''
        for k in range(len(xw)):
            if k not in wordIndexes:
                newXW += xw[k:k+1]
            else:
                newXW += wordList.pop()
        return newXW


def addHword(xw, vPos, hPos, word, width):
    # assumes that the word fits
    # (for now)
    startInd = vPos*width + hPos
    endInd = startInd + width
    if startInd//width != endInd//width:
        print('Word doesn\'t fit in location (H).')
        return -1
    for index in range(startInd, endInd + 1):
        if xw[index] != '-' or '~':
            print('Can\'t add word over non-empty space (H).')
            return -1
    newXW = xw[:startInd] + word + xw[endInd:]
    return newXW


def setIndex(xw, index, character):
    if xw == -1:
        return xw
    if xw[index] == character:
        return xw
    if xw[index] in ('~', '#'):
        return -1
    return xw[:index] + character + xw[index + 1:]


def fillInputs(height, width, hWords, vWords):
     xw = ''.join(['-' for num in range(height*width)])
     for vWord in vWords:
        vPos, hPos, word = vWord
        xw = addVword(xw, vPos, hPos, word, width)
     for hWord in hWords:
         vPos, hPos, word = hWord
         xw = addHword(xw, vPos, hPos, word, width)
     return xw


def protectBoard(xw):
    for index in range(len(xw)):
        if xw[index] not in ('#', '-'):
            # if it's not one of those two its a letter
            xw = setIndex(xw, index, '~')
    return xw


def palindromize(xw):
    length = len(xw)
    for index in range(length):
        if xw[index] == '-' and xw[length - 1 - index] == '#':
            # if the mirror of the cell is blocked and the
            # current one isn't, block it
            xw = setIndex(xw, index, '#')
        elif xw[index] == '#' and xw[length - 1 - index] == '~':
            # if the cell is blocked and its mirror is protected
            # then it's an impossible blocking
            return -1 # impossible crossword
    return xw


def checkEdges(xw, width):
    for index in range(len(xw)):
        if index // width == 0:
            # top row
            if xw[index + width*2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index + width, '#')
                if xw == -1:
                    return xw
            elif xw[index + width] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
        elif index // width == width - 1:
            # bottom row
            if xw[index - width*2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index - width, '#')
                if xw == -1:
                    return xw
            elif xw[index - width] == '#':
                if xw == -1:
                    return xw
        if index % width == 0:
            # left column
            if xw[index + 2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index+1, '#')
                if xw == -1:
                    return xw
            elif xw[index + 1] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
        elif index % width == width - 1:
            # right column
            if xw[index - 2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index - 1, '#')
                if xw == -1:
                    return xw
            elif xw[index - 1] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
    return xw


def checkRest(xw, width, blocks):
    # could be done better with a lookup table like I did in the othello
    # labs, but that would require more debugging and this works
    for index in blocks:
        checkInds = [index - width*3, index - width*2,
                     index + width*3, index + width*2,
                     index - 3, index - 2,
                     index + 3, index + 2]
        skipChecks = set()
        for i in range(8):
            if i in skipChecks: continue
            if xw == -1: return -1
            if 0 <= checkInds[i] < len(xw):
                if xw[checkInds[i]] == '#':
                    if i == 0:
                        xw = setIndex(xw, index - width*2, '#')
                        xw = setIndex(xw, index - width, '#')
                        skipChecks.add(1)
                    elif i == 1:
                        xw = setIndex(xw, index - width, '#')
                    elif i == 2:
                        xw = setIndex(xw, index + width*2, '#')
                        xw = setIndex(xw, index + width, '#')
                        skipChecks.add(3)
                    elif i == 3:
                        xw = setIndex(xw, index + width, '#')
                    elif i  == 4:
                        xw = setIndex(xw, index - 2, '#')
                        xw = setIndex(xw, index - 1, '#')
                        skipChecks.add(5)
                    elif i == 5:
                        xw = setIndex(xw, index - 1, '#')
                    elif i == 6:
                        xw = setIndex(xw, index + 2, '#')
                        xw = setIndex(xw, index + 1, '#')
                        skipChecks.add(7)
                    elif i == 7:
                        xw = setIndex(xw, index + 1, '#')
    return xw


def checkConnected(xw, width, vPos, hPos, numSpaces):
    index = vPos*width + hPos
    if xw == 1: return 1
    if xw.count('*') + xw.count('~') == numSpaces:
        return 1
    if 0 <= index < len(xw) and xw[index] == '-':
        print('CONNECTING')
        xw = setIndex(xw, index, '*')
        xw = checkConnected(xw, width, vPos + 1, hPos, numSpaces)
        xw = checkConnected(xw, width, vPos - 1, hPos, numSpaces)
        xw = checkConnected(xw, width, vPos, hPos + 1, numSpaces)
        xw = checkConnected(xw, width, vPos, hPos - 1, numSpaces)
    if xw != 1: printXW(xw, width)
    return xw


def isValid(xw, numBlocks, width):
    placedBlocks = xw.count('#')
    if placedBlocks > numBlocks:
        #print('TOO MANY BLOCKS')
        return 0
    openSpaces = len(xw) - placedBlocks
    v, h = xw.find('-')//width, xw.find('-') % width
    numConnect = checkConnected(xw, width, v, h, openSpaces)
    #print('NumConnect: {}\nNum \'-\': {}'.format(numConnect, openSpaces))
    if numConnect != 1:
        print('NOT CONNECTED')
        return 0
    return 1


def makeImplications(xw, width, numBlocks):
    if xw == -1: return -1
    #printXW(xw, width)
    xw = checkEdges(xw, width)
    #print('Check edges:')
    if xw == -1: return -1
    #printXW(xw, width)
    blockInds = {i for i in range(len(xw)) if xw[i] == '#'}
    xw = checkRest(xw, width, blockInds)
    if xw == -1: return -1
    #print('Check rest')
    #printXW(xw, width)
    xw = palindromize(xw)
    if xw == -1: return -1
    #print('Palindromize')
    #printXW(xw, width)
    if not isValid(xw, numBlocks, width):
        return -1
    #print('IS VALID')
    #print(xw)
    #printXW(xw, width)
    return xw


def addBlocks(xw, height, width, numBlocks):
    if height%2 + width%2 + numBlocks%2 == 3:
        # if height, width, and numBlocks are
        # odd, then you must place a block in the center
        xw = setIndex(xw, int((len(xw)-1)/2), '#')
        blocksLeft = numBlocks - 1
    else:
        # otherwise make sure not to put block at center
        xw = setIndex(xw, int((len(xw)-1)/2), '~')
        blocksLeft = numBlocks
    availableIndexes = {i for i in range(len(xw)) if xw[i] == '-'}
    #availableIndexes = {0}
    length = len(xw)
    print(blocksLeft, availableIndexes)
    while blocksLeft and availableIndexes:
        newIndex = availableIndexes.pop()
        #print('NEW INDEX', newIndex)
        newXW = setIndex(xw, newIndex, '#')
        newXW = makeImplications(newXW, width, numBlocks)
        if newXW == -1:
            #print('INDEX {} IS INVALID'.format(newIndex))
            availableIndexes.remove(length - newIndex - 1)
        else:
            xw = newXW
            printXW(xw, width)
            blocksLeft = numBlocks - xw.count('#')
    return xw


# create structure
xw = fillInputs(height, width, hWords, vWords)
#printXW(xw, width)
#print('')
xw = protectBoard(xw)
#printXW(xw, width)
#print('')
xw = palindromize(xw)
#printXW(xw, width)
#print('')
xw = addBlocks(xw, height, width, numBlocks)
if xw != -1: printXW(xw, width)
else: print('Impossible')
