import copy
from operator import index

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
        # this part is identical to search
        if len(word) == 0:
            return False
        else:
            curPoint = self
            print("curPoint 1 ", curPoint)
            for i in range(0, len(word)):
                if word[i] not in curPoint.child:
                    return False
                else:
                    curPoint = curPoint.child[word[i]]
                    print("curPoint 2 ", curPoint)
            if not curPoint.wordEnd:
                return False
            # at this point we've found the word if curPoint.wordEnd is true
            # first check if this node has children. If so, just delete wordEnd
            else:
                if len(curPoint.child) > 0:
                    curPoint.wordEnd = False
                    return True
                else:
                    # we need to go up deleting child nodes until we find another
                    # wordEnd or one with more than 0 siblings
                    print("curPoint 3 ", curPoint)
                    while True:
                        parent = curPoint.parent
                        sibs = len(curPoint.parent.child) 
                        print("deleting curPoint 4 ", curPoint)
                        del parent.child[curPoint.value]
                        if sibs > 1 or parent == self or parent.wordEnd:
                            break
                        curPoint = parent      

    
    # search through trie to find word return False or True
    def search(self, word):
        if len(word) == 0:
            return False
        else:
            curPoint = self
            for i in range(0, len(word)):
                if word[i] not in curPoint.child:
                    return False
                else:
                    curPoint = curPoint.child[word[i]]
            return curPoint.wordEnd
    
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

    # delete all child words containing ltr
    def delLetter(self, ltr):
        if self.leaf:
            return []
        else:
            for k in dict(self.child).keys():
                if k == ltr:
                    del self.child[k]
                else:
                    self.child[k].delLetter(ltr)

    
    