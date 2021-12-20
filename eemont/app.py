import json
import webbrowser

import ee
import requests
from box import Box
from bs4 import BeautifulSoup
from ee_extra.Apps.core import apps as extra_apps

from .extending import extend


@extend(ee)
class App:
    """Google Earth Engine App Manager and Descriptor.

    Inspect, open and download Google Earth Engine apps.

    Parameters
    ----------
    url : str
        URL of the Google Earth Engine App.

    Examples
    --------
    >>> import ee, eemont
    >>> app = ee.App("https://jstnbraaten.users.earthengine.app/view/conus-cover-vis")
    >>> app.name
    'conus-cover-vis'
    >>> app.creator
    'jstnbraaten'
    >>> app.open()
    >>> app.download()
    """

    def __init__(self, url):
        if "users.earthengine.app" not in url:
            raise Exception("Not a valid Earth Engine App! Check the url again!")
        if "users.earthengine.app/view/" not in url:
            raise Exception(
                "This seems to be an Earth Engine App Collection! Please use the url of an app!"
            )

        self.url = url
        """URL of the App."""

        self.name = url.split("/")[4]
        """Name of the App."""

        self.creator = url.split("/")[2].split(".")[0]
        """Username of the App creator."""

        self.username = self.creator
        """Instance of creator."""

    def __repr__(self):
        return f"Google Earth Engine App (name: {self.name}, creator: {self.creator})"

    def open(self):
        """Opens the current app in the default browser if possible.

        Returns
        -------
        None

        Examples
        --------
        >>> import ee, eemont
        >>> app = ee.App("https://jstnbraaten.users.earthengine.app/view/conus-cover-vis")
        >>> app.open()
        """
        webbrowser.open(self.url)

    def download(self, file=None):
        """Downloads the current app to a JS file.

        Parameters
        ----------
        file : str, default = None
            Path + filename to store the file. If None, the name of the app is used.

        Returns
        -------
        None

        Examples
        --------
        >>> import ee, eemont
        >>> app = ee.App("https://jstnbraaten.users.earthengine.app/view/conus-cover-vis")
        >>> app.download()
        """
        r = requests.get(self.url)
        r = BeautifulSoup(r.text)
        r = r.find_all("main")[0].find("script").string
        app_url = re.findall(r"init\((.*?)\)", r)[0].replace('"', "").replace("'", "")
        r = requests.get(app_url).json()
        path = r["path"]
        r = r["dependencies"][path]
        if file is None:
            file = self.name + ".js"
        with open(file, "w") as fp:
            fp.write(r)


@extend(ee)
def listApps(online=False):
    """Gets the dictionary of available Google Earth Engine Apps from ee-appshot [1]_.

    Parameters
    ----------
    online : boolean
        Whether to retrieve the most recent list of apps directly from the GitHub
        repository and not from the local copy.

    Returns
    -------
    Box
        Dictionary of available apps.

    Examples
    --------
    >>> import ee, eemont
    >>> apps = ee.listApps()
    >>> apps.jstnbraaten.conus_cover_vis
    Google Earth Engine App (name: conus-cover-vis, creator: jstnbraaten)
    >>> apps.jstnbraaten.conus_cover_vis.name
    'conus-cover-vis'
    >>> apps.jstnbraaten.conus_cover_vis.open()
    >>> apps.jstnbraaten.conus_cover_vis.download()

    References
    ----------
    .. [1] Roy, Samapriya. 2021. ee-appshot: Create Snapshot of Earth Engine Apps.
        https://github.com/samapriya/ee-appshot
    """

    class GoogleEarthEngineApps(Box):
        def __repr__(self):
            return f"Google Earth Engine User Apps (items: {list(self.keys())})"

    ee_apps = extra_apps()
    apps_extra = {}
    for user, eeapps in ee_apps.items():
        apps_extra[user] = {}
        user_apps = []
        for app in eeapps:
            if "users.earthengine.app/view/" in app:
                the_app = App(app)
            apps_extra[user][the_app.name] = the_app

    return GoogleEarthEngineApps(apps_extra, frozen_box=True)
