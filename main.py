from cipher import *

words = '/usr/share/dict/american-english'
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

addWordsToTries('cat ant art ace go frank')
tries[2].walk()
cipherKey = string.ascii_lowercase[1:]+ "a' "
result = Cipher.decrypt('bdf', cipherKey)
print(result)

# Cipher.resetCipherKey()
# attemptCracking('bdf') # ace
# # Cipher.resetCipherKey()
# attemptCracking('dbu') # cat
# attemptCracking('bou')
# quit()
 
# file = open(words, 'r')
# i = 0
# for line in file:
# #     print(line,end='')
#     word = line[:-1]
#     if len(word) == 1 and word[0] != 'a' and word[0] != 'i': 
#         continue
#     else:
#         if not word[0].islower(): continue
# #     print(len(word))
#     addWordsToTries(word)
#     i += 1
#     if (i == 10): print(i)
# print('%d words loaded' % i)
# tries[0].walk()

quote = 'ZMUEK CD IMC AK CDSOV TACV CVM JAZMKOM TACVAK' \
'HDSEJMZX UKL WKDT CVUC MPMEHCVAKI AK CVAJ ZAXM VUJ U FSEFDJM.' #'- MZAJUGMCV WSGZME-EDJJ'
quote=('ab xxx')
print(quote)
cipher = Cipher(quote)
cipher.crackPhrase()