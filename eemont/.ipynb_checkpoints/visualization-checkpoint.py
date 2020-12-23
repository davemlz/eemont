def rgb(platform = 'S2',minValue = 0,maxValue = 0.3,scaled = True):
    '''Create RGB visualization parameters (Red, Green, Blue).
    
    Parameters
    ----------
    platform : string, default = 'S2'
        Satellite platform. Available options:
        - 'S2' : Sentinel 2.
        - 'L8' : Landsat 8.
        - 'L7' : Landsat 7.
        - 'L5' : Landsat 5.
        - 'L4' : Landsat 4.
    minValue : numeric, default = 0
        Min value to stretch the histogram to.
    maxValue : numeric, default = 0.3
        Max value to stretch the histogram to.
    scaled : boolean, default = True
        Wheter the image is scaled to the range [0,1].
        
    Returns
    -------
    dict
        RGB visualization parameters.
    ''' 
    lookup = {
        'S2': ['B4','B3','B2'],
        'L8': ['B4','B3','B2'],
        'L7': ['B3','B2','B1'],
        'L5': ['B3','B2','B1'],
        'L4': ['B3','B2','B1'],
    }
    
    if not scaled:
        minValue = minValue * 1e4
        maxValue = maxValue * 1e4
        
    return {'min':minValue,'max':maxValue,'bands':lookup[platform]}

def infrared(platform = 'S2',minValue = 0,maxValue = 0.6,scaled = True):
    '''Create infrared visualization parameters (NIR, Red, Green).
    
    Parameters
    ----------
    platform : string, default = 'S2'
        Satellite platform. Available options:
        - 'S2' : Sentinel 2.
        - 'L8' : Landsat 8.
        - 'L7' : Landsat 7.
        - 'L5' : Landsat 5.
        - 'L4' : Landsat 4.
    minValue : numeric, default = 0
        Min value to stretch the histogram to.
    maxValue : numeric, default = 0.6
        Max value to stretch the histogram to.
    scaled : boolean, default = True
        Wheter the image is scaled to the range [0,1].
        
    Returns
    -------
    dict
        Infrared visualization parameters.
    ''' 
    lookup = {
        'S2': ['B8','B4','B3'],
        'L8': ['B5','B4','B3'],
        'L7': ['B4','B3','B2'],
        'L5': ['B4','B3','B2'],
        'L4': ['B4','B3','B2'],
    }
    
    if not scaled:
        minValue = minValue * 1e4
        maxValue = maxValue * 1e4
        
    return {'min':minValue,'max':maxValue,'bands':lookup[platform]}

def landwater(platform = 'S2',minValue = 0,maxValue = 0.6,scaled = True):
    '''Create Land/Water visualization parameters (NIR, SWIR1, Red).
    
    Parameters
    ----------
    platform : string, default = 'S2'
        Satellite platform. Available options:
        - 'S2' : Sentinel 2.
        - 'L8' : Landsat 8.
        - 'L7' : Landsat 7.
        - 'L5' : Landsat 5.
        - 'L4' : Landsat 4.
    minValue : numeric, default = 0
        Min value to stretch the histogram to.
    maxValue : numeric, default = 0.6
        Max value to stretch the histogram to.
    scaled : boolean, default = True
        Wheter the image is scaled to the range [0,1].
        
    Returns
    -------
    dict
        Land/Water visualization parameters.
    ''' 
    lookup = {
        'S2': ['B8','B11','B4'],
        'L8': ['B5','B6','B4'],
        'L7': ['B4','B5','B3'],
        'L5': ['B4','B5','B3'],
        'L4': ['B4','B5','B3'],
    }
    
    if not scaled:
        minValue = minValue * 1e4
        maxValue = maxValue * 1e4
        
    return {'min':minValue,'max':maxValue,'bands':lookup[platform]}

def vegetation(platform = 'S2',minValue = 0,maxValue = 0.6,scaled = True):
    '''Create Vegetation visualization parameters (SWIR2, SWIR1, NIR).
    
    Parameters
    ----------
    platform : string, default = 'S2'
        Satellite platform. Available options:
        - 'S2' : Sentinel 2.
        - 'L8' : Landsat 8.
        - 'L7' : Landsat 7.
        - 'L5' : Landsat 5.
        - 'L4' : Landsat 4.
    minValue : numeric, default = 0
        Min value to stretch the histogram to.
    maxValue : numeric, default = 0.6
        Max value to stretch the histogram to.
    scaled : boolean, default = True
        Wheter the image is scaled to the range [0,1].
        
    Returns
    -------
    dict
        Vegetation visualization parameters.
    '''
    lookup = {
        'S2': ['B12','B11','B4'],
        'L8': ['B7','B6','B4'],
        'L7': ['B7','B5','B3'],
        'L5': ['B7','B5','B3'],
        'L4': ['B7','B5','B3'],
    }
    
    if not scaled:
        minValue = minValue * 1e4
        maxValue = maxValue * 1e4
        
    return {'min':minValue,'max':maxValue,'bands':lookup[platform]}

def index(palette = 'vegetation',minValue = 0,maxValue = 1):
    '''Create index visualization parameters.
    
    Parameters
    ----------
    palette : string | list[string], default = 'vegetation'
        Color palette as list of HEX codes or color names. Available options for string type:
        - 'vegetation'
        - 'burn'
        - 'water'
    minValue : numeric, default = -1
        Min value to stretch the histogram to.
    maxValue : numeric, default = 1
        Max value to stretch the histogram to.
        
    Returns
    -------
    dict
        Index visualization parameters.
    ''' 
    lookup = {
        'vegetation': ['118ab2','9a031e','bc6c25','dda15e','fefae0','ecf39e','90a955','4f772d','31572c','132a13'],
        'burn': ['03071e', '6a040f', 'd00000', 'e85d04', 'ffba08'],
        'water': ['bc6c25','caf0f8', '90e0ef', '00b4d8', '0077b6', '03045e'],
    }
    
    if not isinstance(palette, list):
        palette = lookup[palette]
        
    return {'min':minValue,'max':maxValue,'palette':palette}