import ee

def closest(imageCollection,date):

    def setProperties(img):
    # FIRST COMPUTE DATE DIFFERENCE AND DELETE SIGN
    img = img.set('dateDist',ee.Number(img.get('system:time_start')).subtract(date.millis()).abs())
    # SAVE THE DAY TO GET ALL IMAGES IN THE REGION FROM THE SAME DAY
    img = img.set('day',ee.Date(img.get('system:time_start')).get('day')) 
    return img

    # MAP THE PREVIOUS FUNCTION
    imageCollection = imageCollection.map(setProperties).sort('dateDist')
    # GET THE DAY OF THE CLOSEST IMAGE TO THE FLOOD EVENT
    dayToFilter = ee.Date(imageCollection.limit(1).first().get('system:time_start')).get('day')
    # FILTER COLLECTION BY THAT DAY
    imageCollection = imageCollection.filter(ee.Filter.eq('day',dayToFilter))

    return imageCollection