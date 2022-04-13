import copy

WORDLEN = 5

# the solution words are placed in this trie

class Trie(object):

    index = 0

    def __init__(self):
        self.index = Trie.index
        if self.index == 0:
            self.value = "ROOT"
        else:
            self.value = ""
        Trie.index = Trie.index + 1
        self.parent = {}
        self.child = {}
        self.wordEnd = False

    def __repr__(self):
        s = "{index: " + str(self.index) + ", "
        s = s + "value: " + self.value + ", "
        s = s + "wordEnd: " + str(self.wordEnd) + ", "
        s = s + "child#: " + str(len(self.child)) + "}"
        return s
    
    # Insert a word using self as the root
    def insert(self, word):
        if len(word) == 0:
            return False
        else:
            curPoint = self
            for i in range(0, len(word)):
                if word[i] not in curPoint.child:
                    newChild = Trie()
                    newChild.value = word[i]
                    newChild.parent = curPoint
                    newChild.wordEnd = False
                    curPoint.child[word[i]] = newChild
                curPoint = curPoint.child[word[i]]                    
            curPoint.leaf = True
            curPoint.wordEnd = True
            return True

    # Delete a word from child of self
    # Returns True if deleted and False if not found
    def delete(self, word):
        result = self.search(word)
        if result == -1:
            return False
        else:
            # at this point we've found the word and result.wordEnd is true
            # first check if this node has children. If so, just delete wordEnd
            if len(result.child) > 0:
                result.wordEnd = False
                return True
            else:
                # we need to go up deleting child nodes until we find another
                # wordEnd or one with other siblings
                while True:
                    parent = result.parent
                    sibs = len(result.parent.child) 
                    del parent.child[result.value]
                    if sibs > 1 or parent == self or parent.wordEnd:
                        break
                    result = parent      
            return True


    # search through trie to find word 
    # if not found, return -1
    # if found return node pointing to end of word
    def search(self, word):
        if len(word) == 0:
            return -1
        else:
            curPoint = self
            for i in range(0, len(word)):
                if word[i] not in curPoint.child:
                    return -1
                else:
                    curPoint = curPoint.child[word[i]]
            if not curPoint.wordEnd:
                return -1
            else:
                return curPoint
    
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

    # delete all child words that DO NOT contain letter at any position
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
    def delNNLetter(self, ltr, posn):
        returnVal = False
        curPoint = self
        if posn == 0:
            for c in copy.copy(curPoint.child):
                if c != ltr:
                    del curPoint.child[c]
                    returnVal = True
        # if posn not 0, apply this method to children
        else:
            for c in copy.copy(curPoint.child):
                x = curPoint.child[c].delNNLetter(ltr, posn - 1)
                if x:
                    returnVal = True
        return returnVal
        

    # return trie node given index
    # recursively search through trie to find record with specific index
    # returns -1 if no such record
    def getIndex(self, idx):
        if self.index == idx:
            return self
        elif len(self.child) == 0:
            return -1
        else:
            for c in self.child:
                x = self.child[c].getIndex(idx)
                if x != -1:
                    return x
            return -1

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
                if self.child[k].wordEnd:
                    nsuffixes = nsuffixes + [k]
                returnVal = returnVal + nsuffixes
            return returnVal
