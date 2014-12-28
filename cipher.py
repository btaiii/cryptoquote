import string

DEBUG = True
LONGEST_WORD = 23
UNENCRYPTED_CHARS = "' .-"
TARGET_STRING = string.ascii_lowercase + UNENCRYPTED_CHARS
TARGET_SET = set( TARGET_STRING )
NUM_CHARACTERS = len(TARGET_STRING)
NUM_ENCRYPTED_CHARACTERS = NUM_CHARACTERS - len(UNENCRYPTED_CHARS)
NO_TRANSLATION = '*'
BLANK_CIPHER_KEY = NO_TRANSLATION * (NUM_ENCRYPTED_CHARACTERS) + UNENCRYPTED_CHARS
# LETTER_FREQUENCIES = 'etaoinshrdlcumwfgypbvkjxqz'
    
def addWordsToTries(words):
    for word in words.split():
        tries[len(word)-1].add(word)

def addWordToTries(word):
    tries[len(word)-1].add(word)
    
def attemptCracking(word):
    result = tries[len(word)-1].crack(word, [ ], [ [] ])
    print('word: ' + word + ', result: ' + str(result))
                
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
                
    def crack(self, word, words, cipherKey):
        crackedChar = Cipher.decryptChar(word[0], cipherKey)
        if crackedChar != -1:       # this character has been tentatively cracked
            index = Node.indexOfChar(crackedChar)
            if len(word) == 1:      # end of word ... is this word in the trie?
                if self.children[index] == None:
                    return False
                else:
                    if len(words) == 0:
                        return True
                    else:
                        if tries[len(words[0])-1].crack(words[0], words[1:], cipherKey):
                            return True
            if self.children[index] == None:
                return False
            return self.children[index].crack(word[1:], words, cipherKey)
        else:                       # this character has no Cracking yet
            if DEBUG:
                print("Selecting a translation for " + word[0], end=': ')
            for index in range(NUM_CHARACTERS):
            # choose a letter that is a potential match and doesn't already have a mapping
# TODO a letter can't represent itself
                if self.children[index] != None and \
                    cipherKey[index] == NO_TRANSLATION and cipherKey.find(word[0]) == -1:
                    cipherKey = cipherKey[:index] + word[0] + cipherKey[index+1:]
                    if DEBUG:
#                         print('Decisions: ' + str(decisionPoints))
                        print(TARGET_STRING[index] + ' |' + cipherKey + '|')
                    if len(word) == 1:
                        if len(words) == 0:
                            return True
                        else:
                            if tries[len(words[0])-1].crack(words[0], words[1:], cipherKey):
                                return True
                    if self.children[index] == None:
                        return False
                    print(self.charPath, self.children[index], word, words, cipherKey)
                    if self.children[index].crack(word[1:], words, cipherKey): 
                        return True
            if DEBUG:
                print('No possible translation')
            # no further letters available to try
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
        self.words = phrase.lower().split()
        # http://stackoverflow.com/questions/12791501/python-initializing-a-list-of-lists
        # [ [] ] * len(self.words) gives a list of references to the same list
        self.decisionPoints = [[] for _ in range(len(self.words))]
        
    def crackPhrase(self):
        self.crack()
        
    def crack(self):
        word = self.words[0]
        result = tries[len(word)-1].crack(word, self.words[1:], BLANK_CIPHER_KEY)
        print(result)
#         print('word: ' + word + ', result: ' + str(result))
        
    @staticmethod
    def resetCipherKey():
        Cipher.cipherKey = BLANK_CIPHER_KEY
        Cipher.decisionPoints = []
        
    @staticmethod
    def is_valid(word):
        return set(word).issubset(TARGET_SET)
    
    @staticmethod
    def decrypt(word, cipherKey):
        result = [Cipher.decryptChar(char, cipherKey) for char in word]
        return word, ''.join(result)
    
    @staticmethod
    def decryptChar(char, cipherKey):
        crackedIndex = cipherKey.find(char)
        if crackedIndex == -1: return -1
        return TARGET_STRING[crackedIndex]
    
tries = [Trie(i+1) for i in range(LONGEST_WORD)]
