import ee
import warnings

def _extend_eeNumber():
    """Decorator. Extends the ee.Number class."""
    return lambda f: (setattr(ee.ee_number.Number,f.__name__,f) or f)

@_extend_eeNumber()
def __add__(self, other):
    '''Computes the addition between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Addition of two numbers.
    '''
    return self.add(other)

@_extend_eeNumber()
def __radd__(self, other):
    '''Computes the addition between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Addition of two numbers.
    '''
    return self.add(other)

@_extend_eeNumber()
def __sub__(self, other):
    '''Computes the subtraction between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Subtraction of two numbers.
    '''
    return self.subtract(other)

@_extend_eeNumber()
def __rsub__(self, other):
    '''Computes the subtraction between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Subtraction of two numbers.
    '''
    return ee.Number(other).subtract(self)

@_extend_eeNumber()
def __mul__(self, other):
    '''Computes the multiplication between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Multiplication of two numbers.
    '''
    return self.multiply(other)

@_extend_eeNumber()
def __rmul__(self, other):
    '''Computes the multiplication between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Multiplication of two numbers.
    '''
    return self.multiply(other)

@_extend_eeNumber()
def __truediv__(self, other):
    '''Computes the division between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Division of two numbers.
    '''
    return self.divide(other)

@_extend_eeNumber()
def __rtruediv__(self, other):
    '''Computes the division between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Division of two numbers.
    '''
    return ee.Number(other).divide(self)

@_extend_eeNumber()
def __floordiv__(self, other):
    '''Computes the floor division of two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Floor division of two numbers.
    '''
    return self.divide(other).floor()

@_extend_eeNumber()
def __rfloordiv__(self, other):
    '''Computes the floor division of two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Floor division of two numbers.
    '''
    return ee.Number(other).divide(self).floor()

@_extend_eeNumber()
def __mod__(self, other):
    '''Computes the modulo of two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Modulo of two numbers.
    '''
    return self.mod(other)

@_extend_eeNumber()
def __rmod__(self, other):
    '''Computes the modulo of two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value. 

    Returns
    -------
    ee.Number
        Modulo of two numbers.
    '''
    return ee.Number(other).mod(self)

@_extend_eeNumber()
def __pow__(self, other):
    '''Computes the base (left operand) to the power (right operand).

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Bsae to the power of two numbers.
    '''
    return self.pow(other)

@_extend_eeNumber()
def __rpow__(self, other):
    '''Computes the base (left operand) to the power (right operand).

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Base to the power of two numbers.
    '''
    return ee.Number(other).pow(self)

@_extend_eeNumber()
def __lshift__(self, other):
    '''Computes the left shift operation between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Left shift operation.
    '''
    return self.leftShift(other)

@_extend_eeNumber()
def __rlshift__(self, other):
    '''Computes the left shift operation between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Left shift operation.
    '''
    return ee.Number(other).leftShift(self)

@_extend_eeNumber()
def __rshift__(self, other):
    '''Computes the right shift operation between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Right shift operation.
    '''
    return self.rightShift(other)

@_extend_eeNumber()
def __rrshift__(self, other):
    '''Computes the right shift operation between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Right shift operation.
    '''
    return ee.Number(other).rightShift(self)

@_extend_eeNumber()
def __and__(self, other):
    '''Computes the binary operator AND between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Binary operator AND.
    '''
    return self.And(other)

@_extend_eeNumber()
def __rand__(self, other):
    '''Computes the binary operator AND between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Binary operator AND.
    '''
    return ee.Number(other).And(self)

@_extend_eeNumber()
def __or__(self, other):
    '''Computes the binary operator OR between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Binary operator OR.
    '''
    return self.Or(other)

@_extend_eeNumber()
def __ror__(self, other):
    '''Computes the binary operator OR between two numbers.

    Parameters
    ----------
    self : ee.Number
        Right operand.
    other : ee.Number | numeric 
        Left operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Binary operator OR.
    '''
    return ee.Number(other).Or(self)

@_extend_eeNumber()
def __lt__(self, other):
    '''Computes the rich comparison LOWER THAN between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison LOWER THAN.
    '''
    return self.lt(other)

@_extend_eeNumber()
def __le__(self, other):
    '''Computes the rich comparison LOWER THAN OR EQUAL between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison LOWER THAN OR EQUAL.
    '''
    return self.lte(other)

@_extend_eeNumber()
def __eq__(self, other):
    '''Computes the rich comparison EQUAL between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison EQUAL.
    '''
    return self.eq(other)

@_extend_eeNumber()
def __ne__(self, other):
    '''Computes the rich comparison NOT EQUAL THAN between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison NOT EQUAL.
    '''
    return self.neq(other)

@_extend_eeNumber()
def __gt__(self, other):
    '''Computes the rich comparison GREATER THAN between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison GREATER THAN.
    '''
    return self.gt(other)

@_extend_eeNumber()
def __ge__(self, other):
    '''Computes the rich comparison GREATER THAN OR EQUAL between two numbers.

    Parameters
    ----------
    self : ee.Number
        Left operand.
    other : ee.Number | numeric 
        Right operand. If numeric, an ee.Number is created from its value.

    Returns
    -------
    ee.Number
        Rich comparison GREATER THAN OR EQUAL.
    '''
    return self.gte(other)

@_extend_eeNumber()
def __neg__(self):
    '''Computes the unary operator NEGATIVE on an image.

    Parameters
    ----------
    self : ee.Number
        Operand.

    Returns
    -------
    ee.Number
        Unary operator NEGATIVE.
    '''
    return self.multiply(-1)

@_extend_eeNumber()
def __invert__(self):
    '''Computes the unary operator NOT on an image.

    Parameters
    ----------
    self : ee.Number
        Operand.

    Returns
    -------
    ee.Number
        Unary operator NOT.
    '''
    return self.Not()