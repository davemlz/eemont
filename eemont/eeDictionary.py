import ee
import warnings
from .extending import extend


@extend(ee.dictionary.Dictionary)
def __contains__(self, key):
    '''Returns True if the key is in the dictionary.

    Parameters
    ----------
    self : ee.Dictionary
        Dictionary to check.
    key : item
        Item to check.

    Returns
    -------
    boolean
        Whether the key is contained in the dictionary.
    '''
    return self.contains(key).getInfo()


@extend(ee.dictionary.Dictionary)
def __getitem__(self, key):
    '''Gets the item of the dictionary according to the specified key.

    Parameters
    ----------
    self : ee.Dictionary
        Dictionary to get the items from.
    key : str
        Key used to get the specified item. It gets the value of the specified key.

    Returns
    -------
    ee.Element
        Selected value.
    '''
    return self.get(key)