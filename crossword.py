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
    return xw[:index] + character + xw[index + 1:]


def fillInputs(height, width, hWords, vWords):
     xw = ''.join(['-' for num in range(height*width)])
     for vWord in vWords:
        vPos, hPos, word = vWord
        xw = addVword(xw, vPos, hPos, word, width)
     for hWord in hWords:
         vPos, hPos, word = hWord
         xw = addHword(xw, vPos, hPos, word, width)
     printXW(xw, width)
     return xw


def protectBoard(xw):
    for index in xw:
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


def addBlocks(xw, height, width, numBlocks):
    if height%2 + width%2 + numBlocks%2 == 3:
        # if height, width, and numBlocks are
        # odd, then you must place a block in the center
        xw = setIndex(xw, int(len(xw)-1)/2, '#')
        numBlocks = numBlocks - 1
    else:
        # otherwise make sure not to put block at center
        xw = setIndex(xw, int(len(xw)-1)/2, '~')

    block3 = set() # 3rd blocks away from the border
    for index in range(len(xw)):
        if index//width in (3, height - 3):
            block3.add(index)
        elif index % width in (2, width - 3):
            block3.add(index)
        else: continue
    print(block3)


# create structure
fillInputs(height, width, hWords, vWords)
