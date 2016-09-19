from collections import Counter
from sets import Set
import getpass
import re


PATTERN_CHUNK = 4


# Factor formula found from:
# http://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


# function to rotate letters in text based on some key, Dec is boolean to decrement or not
def rotText(text, key, decrypt=False):
    word = ""
    it = 0
    for c in text:
        if c == ' ':
            word += c
            continue
        # getting the key
        k = key[it]

        if decrypt:
            word += chr(97 + (((ord(c) - 97) - (ord(k) - 97)) % 26))
        else:
            word += chr(97 + (((ord(c) - 97) + (ord(k) - 97)) % 26))

        # Incrementing the Iterator and wrapping if we go over
        it = (it + 1) % len(key)
    return word


# Super Slow?
def findPattern(text):
    matches = []
    for num in range(0, len(text) - PATTERN_CHUNK):
        substring = text[num: num + PATTERN_CHUNK]
        pattern = re.compile(substring)
        list = pattern.findall(text)
        if len(list) > 1:
            tup = (list[0], len(list))
            matches.append(tup)
    return Set(matches)


def lengthBetween(aSet, text):
    firstPos = 0
    distanceList = []
    for matches in aSet:
        firstPos = text.index(matches[0])
        secondPos = text.index(matches[0], firstPos + PATTERN_CHUNK)
        distanceList.append(secondPos - firstPos)
    return Set(distanceList)


def getEstimatedKeyLength(text):
    repLengthList = []
    for repLength in lengthBetween(findPattern(text), text):
        repLengthList.extend(factors(repLength))

    # Tally up possible key lengths
    return Counter(repLengthList)

# Loops through a piece of text and making a list of strings of size, with spaces not counted as a part of size
def chunkText(text, size):
    chunks = []
    aChunk = ""
    i = 0
    for c in text:
        aChunk += c
        if c is not ' ':
            i += 1
        if i == size:
            chunks.append(aChunk)
            aChunk = ""
            i = 0

    return chunks



filename = "C:\Users\%s\OneDrive\Documents\Carleton\Fifth Year\COMP 4109\Challenge 1\cipher25.txt" % getpass.getuser()

# print rotText('aaaa bbbb cccc', "ccbbe", True)

with open(filename, 'r') as infile:
    cipherText = infile.read().replace('\n', ' ')

# print cipherText
wordbank = cipherText.split()
letterBank = cipherText.replace(' ', '')
estimatedKeyLengthCount = getEstimatedKeyLength(letterBank).most_common()

# Filtering out too weak keys, basically anything that is size 3 or under
estimatedKeyLengthCount = filter(lambda x: x[0] > 3, estimatedKeyLengthCount)
print "Estimated Keys"
print estimatedKeyLengthCount
# Getting the most common size
estimatedKeyA = estimatedKeyLengthCount[0][0]
estimatedKeyB = estimatedKeyLengthCount[1][0]

#Dividing up our message into characters of these chunks,
# leaving spaces in to identify short words to be able to run rotation tests on for frequency of letters
chunkList = chunkText(cipherText, estimatedKeyA)
chunkListB = chunkText(cipherText, estimatedKeyB)
print "CHUNK LIST"
print chunkList
print chunkListB

freqWord = Counter(wordbank)
freqLetter = Counter(letterBank)
cipherLength = len(letterBank)
letters = freqLetter.most_common(3)

# for letter in letters:
#     print rotText(letter[0], "e", True)

threeLetters = []
singles = []
# print list
for w in wordbank:
    if len(w) == 3:
        threeLetters.append(rotText(w, "the", True))
    if len(w) == 1:
        singles.append((w, rotText(w, "I", True)))
print 'SINGLES: '
print singles
print '3 Letter Counts: '
print Counter(threeLetters).most_common()
# get the letters out of the string of "the"
charList = []
for w in threeLetters:
    for c in w:
        charList.append(c)
print 'MOST COMMON CHARS IN 3 LETTERS'
print Counter(charList).most_common()

print 'ORIGINAL TEXT'
print cipherText
print 'DECODED TEXT'
print rotText(cipherText, "rbga", True)
print rotText(cipherText, "aagaraaa", True)
print rotText(cipherText, "sugaraaa", True)
print rotText(cipherText, "sugarbun", True)
