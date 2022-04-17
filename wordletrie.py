import copy

WORDLEN = 5

# the solution words are placed in this trie

class Trie(object):

    # Indexed dict of Trie nodes = {}
    Node = {}
    
    index = 0

    def __init__(self):
        self.index = Trie.index
        if self.index == 0:
            self.value = "ROOT"
        else:
            self.value = ""
        Trie.Node[self.index] = self
        Trie.index = Trie.index + 1
        self.parent = {}
        self.child = {}
        self.level = -1
        

    def __repr__(self):
        s = "{index: " + str(self.index) + ", "
        s = s + "value: " + self.value + ", "
        s = s + "level: " + str(self.level) + ", "
        s = s + "child#: " + str(len(self.child)) + "}"
        return s
    
    # Make new node
    def makeNewNode(self, newLetter):
        print('create new child for ', newLetter)
        newChild = Trie()
        newChild.value = newLetter
        newChild.parent[self.value] = self
        newChild.level = self.level + 1
        self.child[newLetter] = newChild
        Trie.Node[newChild.index] = newChild

    # Insert a letter below the current node 
    def insertLtr(self, newLetter):
        if len(newLetter) != 1:
            return False
        if newLetter in self.child:
            return True
        print('create new child for ', newLetter)
        newChild = Trie()
        newChild.value = newLetter
        newChild.parent[self.value] = self
        newChild.level = self.level + 1
        self.child[newLetter] = newChild
        Trie.Node[newChild.index] = newChild
        return True

    # Insert a word using self as the root
    def insert(self, word):
        if len(word) != WORDLEN:
            return False
        else:
            curPoint = self
            for letter in word:
                result = curPoint.insertLtr(letter)
                if result == False:
                    return False
                curPoint = curPoint.child[letter]
            return True

    # Delete a word from child of self
    # Returns True if deleted and False if not found
    def delete(self, word):
        result = self.search(word)
        if result == -1:
            return False
        else:
            # at this point we've found the word 
            # we need to go up deleting child nodes as long
            # as there are no chidlren and only one parent
            curPoint = result
            for i in range(WORDLEN - 1, -1, -1):
                parents = curPoint.parent
                children = curPoint.child
                if len(children) > 0:
                    break
                del parents[word[i]]
                if len(parents) > 0:
                    break
                if len(parents) > 1 or parents[result.value] == self:
                    break
                result = parents[result.value]     
            return True

    # search through trie to find word 
    # if not found, return -1
    # if found return node pointing to end of word
    def search(self, word):
        if len(word) != WORDLEN:
            return -1
        else:
            curPoint = self
            for letter in word:
                if letter not in curPoint.child:
                    return -1
                else:
                    curPoint = curPoint.child[letter]
            return curPoint
    """
    # delete all child words containing ltr
    # go through children and delete any nodes starting with letter
    # if not starting with letter, recursively call delLetter on children
    # returns False if nothing deleted, True othewise
    def delLetter(self, ltr):
        returnVal = False
        curPoint = self
        # necessary to copy this because in loop we're modifying curPoint.child
        for c in copy.copy(curPoint.child):
            if c == ltr:
                del curPoint.child[c]
                returnVal = True
            else:
                x = curPoint.child[c].delLetter(ltr)
                if x:
                    returnVal = True
        return returnVal
    
    # delete all child words containing ltr in position posn
    # returns True if something deleted, False otherwise
    def delLetterPos(self, ltr, pos):
        returnVal = False
        curPoint = self
        if pos == 0:
            for c in copy.copy(curPoint.child):
                if c == ltr:
                    del curPoint.child[c]
                    returnVal = True
        # if posn not 0, apply this method to children
        else:
            for c in copy.copy(curPoint.child):
                x = curPoint.child[c].delLetterPos(ltr, pos - 1)
                if x:
                    returnVal = True
        return returnVal

    # delete all child words that DO NOT contain letter at any position
    # returns True if anything deleted othwerise False
    def delNLetter(self, ltr):
        returnVal = False
        curPoint = self
        for c in copy.copy(curPoint.child):
            # if we see letter, no need to go further into children of that one
            if c == ltr:
                continue
            # if we've reached word end without letter, delete this one
            elif curPoint.child[c].wordEnd:
                del curPoint.child[c]
                returnVal = True
            else:
                # otherwise, apply this method to child
                x = curPoint.child[c].delNLetter(ltr)
                if x:
                    returnVal = True
        return returnVal

    # delete all child words that DO NOT contain letter at nth child position (0 is immediate child)
    def delNLetterPos(self, ltr, pos):
        returnVal = False
        curPoint = self
        if pos == 0:
            for c in copy.copy(curPoint.child):
                if c != ltr:
                    del curPoint.child[c]
                    returnVal = True
        # if pos not 0, apply this method to children
        else:
            for c in copy.copy(curPoint.child):
                x = curPoint.child[c].delNLetterPos(ltr, pos - 1)
                if x:
                    returnVal = True
        return returnVal
        
"""

    # return list of all words in trie
    # recursively find suffixes pointed to by child record
    # of self, building list of all words and returning that
    def allWords(self):
        if len(self.child) == 0:
            return []
        else:
            returnVal = []
            for k in self.child:
                rsuffixes = self.child[k].allWords()
                # create list expansion with k and each member of rsuffixes
                nsuffixes = [k + r for r in rsuffixes]
                # if we're at end of word, also add this letter
                # since this will be end of a new word
                if self.child[k].level == WORDLEN - 1:
                    nsuffixes = nsuffixes + [k]
                returnVal = returnVal + nsuffixes
            return returnVal
