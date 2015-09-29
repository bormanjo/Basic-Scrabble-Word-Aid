
scrabbleScores = [ ["a", 1], ["b", 3], ["c", 3], ["d", 2], ["e", 1], ["f", 4], ["g", 2], ["h", 4], ["i", 1], ["j", 8], ["k", 5], ["l", 1], ["m", 3], ["n", 1], ["o", 1], ["p", 3], ["q", 10], ["r", 1], ["s", 1], ["t", 1], ["u", 1], ["v", 4], ["w", 4], ["x", 8], ["y", 4], ["z", 10] ]

def letterScore(letter, scorelist):
    '''returns the associated score for the given letter'''
    if letter == scorelist[0][0]:
        return scorelist[0][1]
    else:
        return letterScore(letter, scorelist[1:])
    
def wordScore(word, scorelist):
    '''returns the sum of each letters scores in the word'''
    if word == [] or word == '':
        return 0
    return letterScore(word[0], scorelist) + wordScore(word[1:], scorelist)

def isWord(word, rack):
    '''returns a nuerical value for the number of characters in word that exist in rack'''
    if word == [] or word == '':
        return False
    elif word[0] in rack:
        return True + isWord(word[1:], rack)
    else:
        return isWord(word[1:], rack)

def dictFilter(s, rack):
    '''filters through the dictionary (s) and returns words whose characters (excluding doubles) exist in rack'''
    if s == [] or s == '':
        return []
    elif isWord(s[0], rack) == len(s[0]):
        return [s[0]] + dictFilter(s[1:], rack)
    else:
        return dictFilter(s[1:], rack)

def extraFilter(rack, words):
    '''determines if a possible word can be formed by letters in rack'''
    
    def remove(rack, letter):
        '''returns rack with one character 'letter' removed if it exists in rack'''
        if rack == []:
            return []
        elif rack[0] == letter:
            return rack[1:]
        else:
            return [rack[0]] + remove(rack[1:], letter)
        
    def checkWord(rack, word):
        '''returns True or False if word can be made with letters in rack'''
        if word == '':                              #if the word is empty, that means that all letters have been subtracted                          
            return True                             #from the word and rack, thus word is in rack
        elif word[0] in rack:
            return checkWord(remove(rack, word[0]), word[1:])
        else:
            return False
    
    return filter(lambda x: checkWord(rack, x), words)

def scoreList(rack):
    '''returns the highest scoring word of available list of letters in Rack as recognized in the given Dictionary'''
    possWords = extraFilter(rack, dictFilter(Dictionary, rack))
    possScores = map(lambda x: wordScore(x, scrabbleScores), possWords)

    def makeScoreList(words, scores):
        '''pairs possible words and scores into a list'''
        if words == [] or scores == []:
            return []
        return [[words[0], scores[0]]] + makeScoreList(words[1:], scores[1:])

    return makeScoreList(possWords, possScores)

def bestWord(rack):
    '''returns a list of the highest scoring word'''
    def compareScores(x, y):
        if x[1] >= y[1]:                            #NOTE: if x and y are equal in score, returns x by default
            return x
        elif x[1] < y[1]:
            return y
        
    return reduce(compareScores, scoreList(rack))
