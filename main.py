# crack cryptoquote using tries; Python project
# December, 2014
# Words are organized into a list of tries; each trie in the contains
#   all words of a certain length; the length is 1 plus the index of the trie in the list
# Tries are searched from longest to shortest
from cipher import *

# potential optimizations: 
# 1. choose trie paths in order of letter frequencies
#      For example, if letter is 5% in encrypted phrase, choose letter closes to 5% frequency first

# awk '{ print length(), NR, $0 | "sort -rn" }' american-english | less
# longest word is electroencephalograph's'

# awk '{print length}' input.txt | sort | uniq -c
#      52 1
#     182 2
#     845 3
#    3346 4
#    6788 5
#   11278 6
#   14787 7
#   15674 8
#   14262 9
#   11546 10
#    8415 11
#    5508 12
#    3236 13
#    1679 14
#     893 15
#     382 16
#     176 17
#      72 18
#      31 19
#      10 20
#       3 21
#       5 22
#       1 23

# add a few sample words
# addWordsToTries('cat ant art ace go frank all work and no play can')
# addWordsToTries("AH AS YOU GET OLDER THREE THINGS HAPPEN THE FIRST IS YOUR MEMORY GOES AND I CAN REMEMBER THE OTHER TWO CAN'T")
# load all words from dictionary
Cipher.loadWords()

cipherKey = string.ascii_lowercase[1:]+ "a" + UNENCRYPTED_CHARS
puzzle = Cipher.encrypt('all work and no play cat ant art zombie', cipherKey)

puzzle = 'ZMUEK CD IMC AK CDSOV TACV CVM JAZMKOM TACVAK HDSEJMZX UKL WKDT CVUC MPMEHCVAKI AK CVAJ ZAXM VUJ U FSEFDJM.' #'- MZAJUGMCV WSGZME-EDJJ'

addWordsToTries('kgb lieder')
file = open('quote.txt' , 'r')
puzzle = file.readline()[:-1]


#          not only is the self entwined in society; it owes society its existence in the most literal sense.
#puzzle = "RJS JRUL BX SVH XHUM HRSKBRHI BR XJOBHSL; BS JKHX XJOBHSL BSX HPBXSHROH BR SVH TJXS UBSHCDU XHRXH."

# Show all letters of length 1 or 3
# tries[0].walk()
# tries[2].walk()   
print(puzzle)
cipher = Cipher(puzzle)
if cipher.crack():
    print("Key: " + Cipher.cipherKey)
    decryption = Cipher.decrypt(puzzle.lower(), Cipher.cipherKey)
    print("Decryption:\n      " + puzzle + '\n----> ' + decryption)

# print(Cipher.decrypt('MZAJUGMCV WSGZME-EDJJ', Cipher.cipherKey))