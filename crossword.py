import re
import sys

# crossword assignment v1 due 3/15

# inputs
input = sys.argv[1:]
print('Input:', input)

height, width, numBlocks = 0, 0, 0
wordDict = ''
hWords, vWords = [], []

# test for matches:
# 0 indicates HxW
# 1 indicated number of blocks
# 2 indicates horizontal words
# 3 indicates vertical words
matchTests = [r'^(\d+)x(\d+)$', r'^\d+$', r'^H(\d+)(.+)$', r'^V(\d+)(.+)$']

for arg in input:
    for testNum, matchTest in enumerate(matchTests):
        match = re.search(matchTest, arg, re.I)
        if not match: continue
        if testNum == 0:
            height = int(arg[:arg.lower().find('x')])
            width = int(arg[arg.lower().find('x'):])
        elif testNum == 1:
            numBlocks = int(arg)
        elif testNum == 2:
            hWords.append(arg.lower())
        elif testNum == 3:
            vWords.append(arg.lower())

print('Inputs: \n HxW = {}x{}\n numBlocks = {}\n hWords = {}\n vWords = {}'
      .format(height, width, numBlocks, hWords, vWords))