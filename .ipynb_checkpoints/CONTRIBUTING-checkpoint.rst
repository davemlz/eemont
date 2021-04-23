Contributing
==============

Contributions to eemont are welcome! Here you will find how to do it:

Types
------------------

Bugs
~~~~~~~~~~~

If you find a bug, please report it by opening an issue. if possible, please attach the error, code, version, and other details.

If you want to contributte by fixing an issue, please check the eemont issues: contributions are welcome for open issues with labels :code:`bug` and :code:`help wanted`.

Enhancement
~~~~~~~~~~~

New features and modules are welcome! You can check the eemont issues: contributions are welcome for open issues with labels :code:`enhancement` and :code:`help wanted`.

Documentation
~~~~~~~~~~~~~~~~~~~~~~

You can add examples, notes and references to the eemont documentation by using the NumPy Docstrings of the eemont documentation, or by creating blogs, tutorials or papers.

Steps to follow
------------------

First, fork the `eemont <https://github.com/davemlz/eemont>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
eemont is divided according to Earth Engine classes, and you will find a module for each class (e.g. :code:`imagecollection.py`). Look for the required class as follows:

- ee.Feature: :code:`feature.py`
- ee.FeatureCollection: :code:`featurecollection.py`
- ee.Geometry: :code:`geometry.py`
- ee.Image: :code:`image.py`
- ee.ImageCollection: :code:`imagecollection.py`

The :code:`common.py` is used for methods that can be used for more than one Earth Engine class.

When creating new features, please start with the :code:`self` argument and add the corresponding decorator (e.g. :code:`@_extend_eeImageCollection()`). Check this example:

.. code-block:: python

   @_extend_eeImage()
   def my_new_method(self,other):
        '''Returns the addition of and image and a float.
    
        Parameters
        ----------    
        self : ee.Image [this]
            Image to add.
        other : float
            Float to add.

        Returns
        -------    
        ee.Image
            Addition of an ee.Image and a float.

        Examples
        --------
        >>> import ee, eemont
        >>> ee.Initialize()
        >>> img = ee.Image(0).my_new_method(other = 3.14)
        '''
        return self.add(other)
        
By using the :code:`@_extend_eeImage()` decorator, the :code:`my_new_method()` method is added to the :code:`ee.Image` class. Look for the required decorator as follows:

- ee.Feature: :code:`@_extend_eeFeature()`
- ee.FeatureCollection: :code:`@_extend_eeFeatureCollection()`
- ee.Geometry: :code:`@_extend_eeGeometry()`
- ee.Image: :code:`@_extend_eeImage()`
- ee.ImageCollection: :code:`@_extend_eeImageCollection()`

Remember to use `Black <https://github.com/psf/black>`_!
   
In order to test additions, you can use :code:`pytest` over the :code:`tests` folder::

   pytest tests
   
This will autmatically test all modules for the available satellite platforms through eemont. If you have added a new feature, please include it in the tests.

To test across different Python versions, please use :code:`tox`.

Now it's time to commit your changes and push your development branch::

   git add .
   git commit -m "Description of your work"
   git push origin name-of-dev-branch
  
And finally, submit a pull request.