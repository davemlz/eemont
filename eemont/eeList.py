import ee
import warnings


def _extend_eeList():
    """Decorator. Extends the ee.List class."""
    return lambda f: (setattr(ee.ee_list.List, f.__name__, f) or f)


@_extend_eeList()
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


@_extend_eeList()
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


@_extend_eeList()
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
    return ee.List.repeat(self,other).flatten()


@_extend_eeList()
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
    return ee.List.repeat(self,other).flatten()