# crack cryptoquote using tries; Python project
# December, 2014
# Words are organized into a list of tries; each trie in the contains
#   all words of a certain length; the length is 1 plus the index of the trie in the list
from cipher import *

# potential optimizations: 
# 1. choose trie paths in order of letter frequencies
#      For example, if letter is 5% in encrypted phrase, choose letter closes to 5% frequency first
# 2. start search with longer words

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
# load all words from dictionary
Cipher.loadWords()

cipherKey = string.ascii_lowercase[1:]+ "a" + UNENCRYPTED_CHARS
puzzle = Cipher.encrypt('all work and no play cat ant art zombie', cipherKey)

puzzle = 'ZMUEK CD IMC AK CDSOV TACV CVM JAZMKOM TACVAK' 
'HDSEJMZX UKL WKDT CVUC MPMEHCVAKI AK CVAJ ZAXM VUJ U FSEFDJM.' #'- MZAJUGMCV WSGZME-EDJJ'

# a sample puzzle
# AS YOU GET OLDER THREE THINGS HAPPEN THE FIRST IS YOUR MEMORY GOES AND I CAN'T
# ND VSH OBL SIMBU LKUBB LKAYOD KNJJBY LKB CAUDL AD VSHU XBXSUV OSBD NYM A ENY'L

# REMEMBER THE OTHER TWO
# UBXBXWBU LKB SLKBU LQS.

# add words to puzzle so above puzzle can be solved
# addWordsToTries("AH AS YOU GET OLDER THREE THINGS HAPPEN THE FIRST IS YOUR MEMORY GOES AND I CAN REMEMBER THE OTHER TWO CAN'T")
puzzle = "ND VSH OBL SIMBU LKUBB LKAYOD KNJJBY.  LKB CAUDL AD VSHU XBXSUV OSBD, NYM A ENY'L UBXBXWBU LKB SLKBU LQS."
puzzle = "R OROC'I LCQA RW RI AQPYO HX B  QCX, QN ASBI ISX FIBUXF AQPYO HX, HPI R BYABTF FBA JTFXYW BF B YRWXIRJX JPFRZRBC BCO FQCUANRIXN."

# following puzzle needs 'LIEDER' to solve
# program finds 'LIEDER SINKER' rather than 'LIEDER SINGER'
addWordsToTries('LIEDER')
puzzle = "SNK X KGXRA XK XJ VUWY QXIIXFNEK KU QU L FLWYYW LJ L EXYQYW JXRBYW, LRQ KGYWY GLPY SYYR EYJJ EXYQYW JXRBYWJ."

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
    print("Decryption:\n      " + decryption[0] + '\n----> ' + decryption[1])