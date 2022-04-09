import copy

WORDLEN = 5

# the solution words are placed in this trie

class Trie(object):

    def __init__(self):
        self.value = ''
        self.level = 0
        self.child = {}
        self.wordEnd = False
        self.leaf = True

    def __repr__(self):
        s = "{value: " + self.value + ", "
        s = s + "{level: " + str(self.level) + ", "
        s = s + "{wordEnd: " + str(self.wordEnd) + ", "
        s = s + "{leaf: " + str(self.leaf) + ", "
        s = s + "{child: " + str(self.child) + "}"
        return s
    

    # Insert a word using self as the root
    def insert(self, word):
        # if word is empty, set word end and we're done
        if word == "":
            self.wordEnd = True
        # if already have child with that key, return insertion of remainder of word
        elif word[0] in self.child.keys():
            self.child[word[0]].insert(word[1:])
        # otherwise, add a new node for letter and make same recursive call for rest of word
        else:
            self.child[word[0]] = Trie()
            self.child[word[0]].value = word[0]
            self.child[word[0]].level = self.level + 1
            self.leaf = False
            self.child[word[0]].insert(word[1:])

    def search(self, word):
        if len(word) == 0:
            return self.wordEnd
        else:
            if word[0] not in self.child:
                return False
            else:
                return self.child[word[0]].search(word[1:])
    
    # recursively travel through Trie, returning a list of all words (actually suffixes)
    # that are defined in the Trie
    #   There are two cases:
    #       - leaf - return an empty list
    #       - not leaf - 
    #           - for each letter key in the current object:
    #               - create a list of words by pre-pending the current letter key
    #                 to the list of words returned by recursive call to this method for the Trie
    #                 linked to the letter key
    #           - combine all these lists together and return
    def returnWords(self):
        if self.leaf:
            return []
        else:
            returnVal = []
            for k in self.child.keys():
                rsuffixes = self.child[k].returnWords()
                # create list expansion with k and each member of rsuffixes
                nsuffixes = [k + r for r in rsuffixes]
                # if we're at end of word, also add this letter
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

    
    # delete all child words WITHOUT a containing letter
    def delFixLetter(self, ltr):
        pass
            
            
            for d in self.child[c].keys() 


        for k in dict(self.child).keys():
            if k == ltr:
                return 
            else:
                self.child[k].delFixLetter(ltr)
        
        
            if self.value == ltr:
                return
            else:
                del self
            return
        else:
            for k in dict(self.child).keys():
                if k != ltr:
                    return self.child[k].delFixLetter()
                else:
                    return

            return self.delFixLetter(ltr)




    


