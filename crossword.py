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

print('Inputs: \n Dictionary: {}\n HxW = {}x{}\n numBlocks = {}\n hWords = {}\n vWords = {}'
      .format(wordDict, height, width, numBlocks, hWords, vWords))


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
            print('Word doesn\'t fit in location.')
        wordIndexes.append(index)
    checkIndexes = {xw[i] for i in wordIndexes}
    if checkIndexes != {'-'}:
        print('Can\'t place word over non-empty space.')
    else:
        newXW = ''
        for k in range(len(xw)):
            if k not in wordIndexes:
                newXW += xw[k:k+1]
            else:
                newXW += wordList.pop()
        return newXW


def fillInputs(height, width, hWords, vWords):
     abc = ['a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']
     xw = ''.join([abc[num] for num in range(height*width)])
     for vWord in vWords:
        vPos, hPos, word = vWord
        xw = addVword(xw, vPos, hPos, word, width)
     print('XW', xw)
     printXW(xw, width)

fillInputs(height, width, hWords, vWords)