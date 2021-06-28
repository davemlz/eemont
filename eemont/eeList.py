import ee
import warnings
from .extending import extend


@extend(ee.ee_list.List)
def __contains__(self, key):
    '''Returns True if the key is in the list.

    Parameters
    ----------
    self : ee.List
        List to check.
    key : item
        Item to check.

    Returns
    -------
    boolean
        Whether the key is contained in the list.
    '''
    return self.contains(key).getInfo()


@extend(ee.ee_list.List)
def __len__(self):
    '''Returns the length of the list.

    Parameters
    ----------
    self : ee.List
        List to get the length from.

    Returns
    -------
    int
        Length of the list.
    '''
    return self.length().getInfo()


@extend(ee.ee_list.List)
def __getitem__(self, key):
    '''Gets the item of the list according to the specified key.

    Parameters
    ----------
    self : ee.List
        List to get the items from.
    key : numeric | list[numeric] | slice
        Key used to get the specified item. If numeric, it gets the item at that index. 
        If list, it gets multiple items. If slice, it calls the slice() method (the step parameter is ignored).

    Returns
    -------
    ee.List | ee.Number
        List or number with the selected items.
    '''
    if isinstance(key,slice):

        if key.start == None:
            start = 0
        else:
            start = key.start

        if key.stop == None:
            stop = self.length()
        else:
            stop = key.stop

        selected = self.slice(start,stop)
        
    elif isinstance(key, list):
        
        selected = ee.List([])
        
        for k in key:
            selected = selected.add(self.get(k))

    else:
        selected = self.get(key)

    return selected


@extend(ee.ee_list.List)
def __add__(self, other):
    """Concatenates the contents of other onto list.

    Parameters
    ----------
    self : ee.List
        Left operand.
    other : ee.List | list
        Right operand.

    Returns
    -------
    ee.List
        Concatenation of two lists.
    """
    return self.cat(other)


@extend(ee.ee_list.List)
def __radd__(self, other):
    """Concatenates the contents of other onto list.

    Parameters
    ----------
    self : ee.List
        Right operand.
    other : ee.List | list
        Left operand.

    Returns
    -------
    ee.List
        Concatenation of two lists.
    """
    return ee.List(other).cat(self)


@extend(ee.ee_list.List)
def __mul__(self, other):
    """Returns a new list containing a list repeated n (other) times.

    Parameters
    ----------
    self : ee.List
        Left operand.
    other : ee.Number | numeric
        Right operand.

    Returns
    -------
    ee.List
        Repeated list.
    """
    return ee.List.repeat(self, other).flatten()


@extend(ee.ee_list.List)
def __rmul__(self, other):
    """Returns a new list containing a list repeated n (other) times.

    Parameters
    ----------
    self : ee.List
        Right operand.
    other : ee.Number | numeric
        Left operand.

    Returns
    -------
    ee.List
        Repeated list.
    """
    return ee.List.repeat(self, other).flatten()
