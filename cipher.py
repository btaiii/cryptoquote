import string
import re

WORD_FILE = '/usr/share/dict/american-english'
# DEBUG = True
DEBUG = False
LONGEST_WORD = 23
UNENCRYPTED_CHARS = "' .-,;"
TARGET_STRING = string.ascii_lowercase + UNENCRYPTED_CHARS
TARGET_SET = set( TARGET_STRING )
NUM_CHARACTERS = len(TARGET_STRING)
NUM_ENCRYPTED_CHARACTERS = NUM_CHARACTERS - len(UNENCRYPTED_CHARS)
NO_TRANSLATION = '*'
BLANK_CIPHER_KEY = NO_TRANSLATION * (NUM_ENCRYPTED_CHARACTERS) + UNENCRYPTED_CHARS
# LETTER_FREQUENCIES = 'etaoinshrdlcumwfgypbvkjxqz'
    
def addWordsToTries(words):
    ''' Add a space-delimited sequence of words to the trie structure; apostrophes allowed '''
    for word in words.split():
        tries[len(word)-1].add(word)

def addWordToTries(word):
    tries[len(word)-1].add(word)
    
class Node(object):
    def __init__(self, charPath):
        self.children = [None] * NUM_CHARACTERS
        self.charPath = charPath
        
    def add(self, word):
        nodeIndex = Node.indexOfChar(word[0])
        # mark end-of-word
        if len(word) == 1:
            self.children[nodeIndex] = self.charPath + word[0]
            return
        
        # word continuation
        childNode = self.children[nodeIndex]
        if not childNode:
            childNode = Node(self.charPath + word[0])
            self.children[nodeIndex] = childNode
        childNode.add(word[1:])
            
    def walk(self, wordSoFar):
        for i in range(NUM_CHARACTERS):
            if not self.children[i]: continue
            wordSoFarWithChar = wordSoFar + TARGET_STRING[i]
            childNode = self.children[i]
            if type(childNode) == str:
                print(wordSoFarWithChar, childNode)
            else:
                childNode.walk(wordSoFarWithChar)
                
    def potentialChildIndex(self, index, cipherKey, charToDecrypt):
        # no children with this index
        if self.children[index] == None: return False
        # child already assigned to another letter
        if cipherKey[index] != NO_TRANSLATION: return False
        # a letter can't represent itself
        if charToDecrypt == TARGET_STRING[index]: return False
        return True
    
    def crack(self, word, words, cipherKey):
        potentialChildIndices = []
        
        crackedIndex = cipherKey.find(word[0])
        if crackedIndex >= 0:
            if self.children[crackedIndex] != None:
                potentialChildIndices = [ crackedIndex ]
        else:
            potentialChildIndices = \
                [index for index in range(len(self.children)) if self.potentialChildIndex(index, cipherKey, word[0])]
        
        for index in potentialChildIndices:
            newCipherKey = cipherKey[:index] + word[0] + cipherKey[index+1:]
            if DEBUG:
                print(word[0] + '>>' + TARGET_STRING[index] + ' |' + newCipherKey + '|')
#                 print(self.charPath, word, words, cipherKey)
            if len(word) == 1:
                if len(words) == 0:
                    Cipher.cipherKey = newCipherKey
                    return True    # BASE CASE: all done ... no letters left
                elif tries[len(words[0])-1].crack(words[0], words[1:], newCipherKey):
                    return True
                else:  # try next letter
                    continue
            if type(self.children[index]) == str:
                print('ERROR --->' + self.children[index])
            if self.children[index].crack(word[1:], words, newCipherKey): 
                return True
        if DEBUG:
            print('No possible translation')
        # BASE CASE: no further letters available to try
        return False
    
    @staticmethod
    def indexOfChar(char):
        if char.islower():   # an optimization
            return ord(char) - ord('a')
        else:
            return TARGET_STRING.find(char)
        
class Trie(object):
    def __init__(self, wordSize):
        self.wordSize = wordSize
        self.root = Node('')
    def add(self,word):
        lcWord = word.lower()
        if not Cipher.is_valid(lcWord):
#             if DEBUG:
#                 print('Bad word: ' + lcWord)
            return
        self.root.add(lcWord)
    def walk(self):
        print('Trie of %d-letter words' % self.wordSize)
        self.root.walk('')
    def crack(self, word, words, cipherKey):
        assert Cipher.is_valid(word)
        return self.root.crack(word, words, cipherKey)

class Cipher(object):
    cipherKey = BLANK_CIPHER_KEY
    
    def __init__(self, phrase):
        Cipher.resetCipherKey()
        self.words = re.sub(r'[,.;]','',phrase).lower().split()
        # http://stackoverflow.com/questions/12791501/python-initializing-a-list-of-lists
        # [ [] ] * len(self.words) gives a list of references to the same list
        self.decisionPoints = [[] for _ in range(len(self.words))]
        
    def crack(self):
        word = self.words[0]
        result = tries[len(word)-1].crack(word, self.words[1:], BLANK_CIPHER_KEY)
        print(result)
        return result
#         print('word: ' + word + ', result: ' + str(result))
        
    @staticmethod
    def resetCipherKey():
        Cipher.cipherKey = BLANK_CIPHER_KEY
        Cipher.decisionPoints = []
        
    @staticmethod
    def is_valid(word):
        return set(word).issubset(TARGET_SET)
        
    @staticmethod
    def encrypt(message, cipherKey):
        return ''.join([TARGET_STRING[cipherKey.find(char)] for char in message])
    
    @staticmethod
    def decrypt(word, cipherKey):
        result = [Cipher.decryptChar(char, cipherKey) for char in word]
        return word, ''.join(result)
    
    @staticmethod
    def decryptChar(char, cipherKey):
        crackedIndex = cipherKey.find(char)
        if crackedIndex == -1: return -1
        return TARGET_STRING[crackedIndex]
    
    @staticmethod
    def loadWords(maxWords = None):
        ''' load words from WORD_FILE into trie structure '''
        file = open(WORD_FILE , 'r')
        i = 0
        for line in file:
        #     print(line,end='')
            word = line[:-1]
            if len(word) == 1 and word[0] != 'a' and word[0] != 'i': 
                continue
            else:
                if not word[0].islower(): continue
        #     print(len(word))
            addWordsToTries(word)
            if maxWords and i >= maxWords: 
                print("Bad word: " + word)
                break
            i += 1
        print('%d words loaded' % i)
    
tries = [Trie(i+1) for i in range(LONGEST_WORD)]
