import warnings

import ee

from .extending import extend


@extend(ee.ee_number.Number)
def __add__(self, other):
    """Computes the addition between two numbers.

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
    """
    return self.add(other)


@extend(ee.ee_number.Number)
def __radd__(self, other):
    """Computes the addition between two numbers.

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
    """
    return self.add(other)


@extend(ee.ee_number.Number)
def __sub__(self, other):
    """Computes the subtraction between two numbers.

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
    """
    return self.subtract(other)


@extend(ee.ee_number.Number)
def __rsub__(self, other):
    """Computes the subtraction between two numbers.

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
    """
    return ee.Number(other).subtract(self)


@extend(ee.ee_number.Number)
def __mul__(self, other):
    """Computes the multiplication between two numbers.

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
    """
    return self.multiply(other)


@extend(ee.ee_number.Number)
def __rmul__(self, other):
    """Computes the multiplication between two numbers.

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
    """
    return self.multiply(other)


@extend(ee.ee_number.Number)
def __truediv__(self, other):
    """Computes the division between two numbers.

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
    """
    return self.divide(other)


@extend(ee.ee_number.Number)
def __rtruediv__(self, other):
    """Computes the division between two numbers.

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
    """
    return ee.Number(other).divide(self)


@extend(ee.ee_number.Number)
def __floordiv__(self, other):
    """Computes the floor division of two numbers.

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
    """
    return self.divide(other).floor()


@extend(ee.ee_number.Number)
def __rfloordiv__(self, other):
    """Computes the floor division of two numbers.

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
    """
    return ee.Number(other).divide(self).floor()


@extend(ee.ee_number.Number)
def __mod__(self, other):
    """Computes the modulo of two numbers.

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
    """
    return self.mod(other)


@extend(ee.ee_number.Number)
def __rmod__(self, other):
    """Computes the modulo of two numbers.

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
    """
    return ee.Number(other).mod(self)


@extend(ee.ee_number.Number)
def __pow__(self, other):
    """Computes the base (left operand) to the power (right operand).

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
    """
    return self.pow(other)


@extend(ee.ee_number.Number)
def __rpow__(self, other):
    """Computes the base (left operand) to the power (right operand).

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
    """
    return ee.Number(other).pow(self)


@extend(ee.ee_number.Number)
def __lshift__(self, other):
    """Computes the left shift operation between two numbers.

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
    """
    return self.leftShift(other)


@extend(ee.ee_number.Number)
def __rlshift__(self, other):
    """Computes the left shift operation between two numbers.

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
    """
    return ee.Number(other).leftShift(self)


@extend(ee.ee_number.Number)
def __rshift__(self, other):
    """Computes the right shift operation between two numbers.

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
    """
    return self.rightShift(other)


@extend(ee.ee_number.Number)
def __rrshift__(self, other):
    """Computes the right shift operation between two numbers.

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
    """
    return ee.Number(other).rightShift(self)


@extend(ee.ee_number.Number)
def __and__(self, other):
    """Computes the binary operator AND between two numbers.

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
    """
    return self.And(other)


@extend(ee.ee_number.Number)
def __rand__(self, other):
    """Computes the binary operator AND between two numbers.

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
    """
    return ee.Number(other).And(self)


@extend(ee.ee_number.Number)
def __or__(self, other):
    """Computes the binary operator OR between two numbers.

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
    """
    return self.Or(other)


@extend(ee.ee_number.Number)
def __ror__(self, other):
    """Computes the binary operator OR between two numbers.

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
    """
    return ee.Number(other).Or(self)


@extend(ee.ee_number.Number)
def __lt__(self, other):
    """Computes the rich comparison LOWER THAN between two numbers.

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
    """
    return self.lt(other)


@extend(ee.ee_number.Number)
def __le__(self, other):
    """Computes the rich comparison LOWER THAN OR EQUAL between two numbers.

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
    """
    return self.lte(other)


@extend(ee.ee_number.Number)
def __eq__(self, other):
    """Computes the rich comparison EQUAL between two numbers.

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
    """
    return self.eq(other)


@extend(ee.ee_number.Number)
def __ne__(self, other):
    """Computes the rich comparison NOT EQUAL THAN between two numbers.

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
    """
    return self.neq(other)


@extend(ee.ee_number.Number)
def __gt__(self, other):
    """Computes the rich comparison GREATER THAN between two numbers.

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
    """
    return self.gt(other)


@extend(ee.ee_number.Number)
def __ge__(self, other):
    """Computes the rich comparison GREATER THAN OR EQUAL between two numbers.

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
    """
    return self.gte(other)


@extend(ee.ee_number.Number)
def __neg__(self):
    """Computes the unary operator NEGATIVE on an image.

    Parameters
    ----------
    self : ee.Number
        Operand.

    Returns
    -------
    ee.Number
        Unary operator NEGATIVE.
    """
    return self.multiply(-1)


@extend(ee.ee_number.Number)
def __invert__(self):
    """Computes the unary operator NOT on an image.

    Parameters
    ----------
    self : ee.Number
        Operand.

    Returns
    -------
    ee.Number
        Unary operator NOT.
    """
    return self.Not()
