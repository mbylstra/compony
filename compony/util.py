import sys

def dictmerge(x, y):
    z = x.copy()
    z.update(y)
    return z

#from http://sourceforge.net/projects/basicproperty/files/basicproperty/0.6.3a/
def flatten(inlist, type=type, ltype=(list,tuple), maxint=sys.maxsize):
    """Flatten out a list."""
    try:
        # for every possible index
        for ind in range(maxint):
            # while that index currently holds a list
            while isinstance(inlist[ind], ltype):
                # expand that list into the index (and subsequent indicies)
                inlist[ind:ind+1] = list(inlist[ind])
            #ind = ind+1
    except IndexError:
        pass
    return inlist

#from http://stackoverflow.com/a/23689767
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__
