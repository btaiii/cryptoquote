'''
Created on Dec 27, 2014

@author: branch
'''
import string
words = '/usr/share/dict/american-english'

def alphabetizedWord(word):
    letters = list(word)
    letters.sort()
    return ''.join(letters)

def solve(word):
    print(sortedWords[alphabetizedWord(word)])
        
file = open(words, 'r')
i = 0
sortedWords = {}
for line in file:
#     print(line,end='')
    word = line[:-1]
    if len(word) not in [5,6] or not word[0].islower(): continue
    sortedWords[alphabetizedWord(word)] = word
    i += 1
#     if (i % 10000 == 0): print(i)
print('%d words loaded' % i)


