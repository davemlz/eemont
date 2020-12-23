import ee
import numpy as np

def closest(collection,date):
    '''Gets the closest image (or set of images) closest to the specified date.
    
    Parameters
    ----------
    collection : ee.ImageCollection
        Image Collection from which to get the closest image to the specified date.
    date : ee.Date | string
        Date of interest. The method will look to images closest to this date.
        
    Returns
    -------
    ee.ImageCollection
        Closest images to the specified date.
    ''' 
    if not isinstance(date, ee.ee_date.Date):
        date = ee.Date(date)
    
    def setProperties(img):        
        img = img.set('dateDist',ee.Number(img.get('system:time_start')).subtract(date.millis()).abs())        
        img = img.set('day',ee.Date(img.get('system:time_start')).get('day')) 
        return img
    
    collection = collection.map(setProperties).sort('dateDist')    
    dayToFilter = ee.Date(collection.limit(1).first().get('system:time_start')).get('day')    
    collection = collection.filter(ee.Filter.eq('day',dayToFilter))
       
    print("Date of the closest image:", np.datetime_as_string(np.datetime64(collection.first().get('system:time_start').getInfo(),'ms')))

    return collection