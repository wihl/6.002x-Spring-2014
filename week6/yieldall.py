# lecture 8 problem 4

class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = float(v)
        self.weight = float(w)
    def getName(self):
        return self.name
    def getValue(self):
        return self.value
    def getWeight(self):
        return self.weight
    def __str__(self):
        result = '<' + self.name + ', ' + str(self.value) + ', '\
                 + str(self.weight) + '>'
        return result

def buildItems():
    names = ['clock', 'painting', 'radio', 'vase', 'book',
             'computer']
    vals = [175,90,20,50,10,200]
    weights = [10,9,4,2,1,20]
    Items = []
    for i in range(len(vals)):
        Items.append(Item(names[i], vals[i], weights[i]))
    return Items



def yieldAllCombos(items):
    """
      Generates all combinations of N items into two bags, whereby each 
      item is in one or zero bags.

      Yields a tuple, (bag1, bag2), where each bag is represented as 
      a list of which item(s) are in each bag.
    """
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in xrange(3**N):
        bag1 = []
        bag2 = []
        for j in xrange(N):
            # test bit jth of integer i
            if (i >> j) % 3 == 0:
                bag1.append(items[j])
            elif (i >> j) % 3 == 1:
                bag2.append(items[j])
            # else pass - do not add to any bag
        yield bag1, bag2


items = buildItems()
combos = yieldAllCombos(items)
for c1, c2 in combos:
    for ca, cb in zip(c1, c2):
        print ca, cb

