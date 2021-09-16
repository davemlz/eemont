import ee
from ee_extra.JavaScript.install import install as ee_install
from ee_extra.JavaScript.install import uninstall as ee_uninstall
from ee_extra.JavaScript.main import ee_require

from .extending import extend


@extend(ee)
def require(module):
    """Loads and executes a JavaScript GEE module.

    All modules must be first installed before requiring them. After requiring the module,
    it can be used in the same way as it is used in the Code Editor.

    Warning
    -------
    This method is highly :code:`experimental`. Please report any irregularities in the
    Issues Page of `eeExtra <https://github.com/r-earthengine/ee_extra>`_.

    Parameters
    ----------
    module : str
        Path to the module in the Code Editor (e.g. "users/dmlmont/spectral:spectral").

    Returns
    -------
    BoxDict
        Loaded module. Methods and attributes can be accessed using dot notation.

    See Also
    --------
    install : Installs a JavaScript GEE module.
    uninstall : Uninstalls a JavaScript GEE module.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> LandsatLST = ee.require("users/sofiaermida/landsat_smw_lst:modules/Landsat_LST.js")
    """
    return ee_require(module)


@extend(ee)
def install(module, update=False, quiet=False):
    """Installs a JavaScript GEE module.

    Warning
    -------
    This method is highly :code:`experimental`. Please report any irregularities in the
    Issues Page of `eeExtra <https://github.com/r-earthengine/ee_extra>`_.

    Parameters
    ----------
    module : str
        Path to the module in the Code Editor (e.g. "users/dmlmont/spectral:spectral").
    update : bool, default = False
        Whether to update the module if it is already installed.
    quiet : bool, default = False
        Whether to show in console the process.

    Returns
    -------
    None

    See Also
    --------
    uninstall : Uninstalls a JavaScript GEE module.
    require : Loads and executes a JavaScript GEE module.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.install("users/sofiaermida/landsat_smw_lst:modules/Landsat_LST.js")
    """
    return ee_install(module, update, quiet)


@extend(ee)
def uninstall(module, quiet=False):
    """Uninstalls a JavaScript GEE module.

    Warning
    -------
    This method is highly :code:`experimental`. Please report any irregularities in the
    Issues Page of `eeExtra <https://github.com/r-earthengine/ee_extra>`_.

    Parameters
    ----------
    module : str
        Path to the module in the Code Editor (e.g. "users/dmlmont/spectral:spectral").
    quiet : bool, default = False
        Whether to show in console the process.

    Returns
    -------
    None

    See Also
    --------
    install : Installs a JavaScript GEE module.
    require : Loads and executes a JavaScript GEE module.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.uninstall("users/sofiaermida/landsat_smw_lst:modules/Landsat_LST.js")
    """
    return ee_uninstall(module, quiet)
