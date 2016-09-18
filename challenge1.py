from collections import Counter
from sets import Set
import getpass
import re


PATTERN_CHUNK = 4

# function to rotate letters in text based on some key, Dec is boolean to decrement or not
def rotText(text, key, dec=False):
    word = ""
    it = 0
    for c in text:
        if c == ' ':
            word += c
            continue
        # getting the key
        k = key[it]

        if dec:
            word += chr(97 + ((ord(c) - ord(k)) % 26))
        else:
            word += chr(97 + ((ord(c) + ord(k)) % 26))

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
    return distanceList



filename = "C:\Users\%s\OneDrive\Documents\Carleton\Fifth Year\COMP 4109\Challenge 1\cipher25.txt" % getpass.getuser()

# print rotText('aaaa bbbb cccc', "ccbbe", True)

with open(filename, 'r') as infile:
    cipherText = infile.read().replace('\n', ' ')

# print cipherText
wordbank = cipherText.split()
letterBank = cipherText.replace(' ', '')
print lengthBetween(findPattern(letterBank), letterBank)

# print wordbank
freqWord = Counter(wordbank)
freqLetter = Counter(letterBank)
cipherLength = len(letterBank)
# print freqLetter
# print cipherLength
letters = freqLetter.most_common(3)

# for letter in letters:
#     print rotText(letter[0], "e", True)
list = list(freqWord)
# print list
# for w in list:
#     if len(w) == 1:
#         print rotText(w, "a", True)

# print rotText(cipherText, "nsug")
