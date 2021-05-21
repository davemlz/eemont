def extend(cls, static=False):
    """Extends the cls class.

    Parameters
    ----------
    cls : class
        Class to extend.
    static : boolean, default = False
        Wheter extend as a static method.

    Returns
    -------
    decorator
        Decorator for extending classes.
    """
    if static:
        return lambda f: (setattr(cls, f.__name__, staticmethod(f)) or f)
    else:
        return lambda f: (setattr(cls, f.__name__, f) or f)
