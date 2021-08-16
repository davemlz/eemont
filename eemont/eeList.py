import warnings

import ee

from .extending import extend


@extend(ee.ee_list.List)
def __contains__(self, key):
    """Returns True if the item is in the list.

    Parameters
    ----------
    self : ee.List
        List to check.
    key : item
        Item to check.

    Returns
    -------
    boolean
        Whether the item is contained in the list.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList = ee.List([1,2,3,5])
    >>> 1 in eeList
    True
    >>> 3 in eeList
    False
    """
    return self.contains(key).getInfo()


@extend(ee.ee_list.List)
def __len__(self):
    """Returns the length of the list.

    Parameters
    ----------
    self : ee.List
        List to get the length from.

    Returns
    -------
    int
        Length of the list.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList = ee.List([1,2,3,5])
    >>> len(eeList)
    4
    """
    return self.length().getInfo()


@extend(ee.ee_list.List)
def __getitem__(self, key):
    """Gets the item of the list according to the specified key.

    Parameters
    ----------
    self : ee.List
        List to get the items from.
    key : numeric | list[numeric] | slice
        Key used to get the specified item. If numeric, it gets the item at that index.
        If list, it gets multiple items. If slice, it calls the slice() method (the step
        parameter is ignored).

    Returns
    -------
    ee.List | ee.Number
        List or number with the selected items.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList = ee.List([1,2,3,5])
    >>> eeList[0].getInfo()
    1
    >>> eeList[0:2].getInfo()
    [1,2,3]
    >>> eeList[0:].getInfo()
    [1,2,3,5]
    >>> eeList[[0,2]].getInfo()
    [1,3]
    """
    if isinstance(key, slice):

        if key.start == None:
            start = 0
        else:
            start = key.start

        if key.stop == None:
            stop = self.length()
        else:
            stop = key.stop

        selected = self.slice(start, stop)

    elif isinstance(key, list):

        selected = ee.List([])

        for k in key:
            selected = selected.add(self.get(k))

    else:
        selected = self.get(key)

    return selected


@extend(ee.ee_list.List)
def __add__(self, other):
    """Concatenates the contents of a list onto another list.

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

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList1 = ee.List([1,2,3,4])
    >>> eeList2 = ee.List([5,6,7,8])
    >>> eeList3 = eeList1 + eeList2
    >>> eeList3.getInfo()
    [1,2,3,4,5,6,7,8]
    """
    return self.cat(other)


@extend(ee.ee_list.List)
def __radd__(self, other):
    """Concatenates the contents of a list onto another list.

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

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList = ee.List([1,2,3,4])
    >>> normalList = [5,6,7,8]
    >>> eeList2 = normalList + eeList
    >>> eeList2.getInfo()
    [5,6,7,8,1,2,3,4]
    """
    return ee.List(other).cat(self)


@extend(ee.ee_list.List)
def __mul__(self, other):
    """Returns a new list containing a list repeated n times.

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

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList1 = ee.List([1,2,3,4])
    >>> eeList2 = eeList * 2
    >>> eeList2.getInfo()
    [1,2,3,4,1,2,3,4]
    """
    return ee.List.repeat(self, other).flatten()


@extend(ee.ee_list.List)
def __rmul__(self, other):
    """Returns a new list containing a list repeated n times.

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

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> eeList1 = ee.List([1,2,3,4])
    >>> eeList2 = 2 * eeList1
    >>> eeList2.getInfo()
    [1,2,3,4,1,2,3,4]
    """
    return ee.List.repeat(self, other).flatten()
