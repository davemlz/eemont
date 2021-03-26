import ee
import warnings
from box import Box

def _get_expression_map(img, platformDict):
    '''Gets the dictionary required for the map parameter in ee.Image.expression() method.
    
    Parameters
    ----------
    img : ee.Image
        Image to get the dictionary from.
    platformDict : dict
        Dictionary retrieved from the _get_platform() method.
        
    Returns
    -------
    dict
        Map dictionary for ee.Image.expression.
    '''        
    def lookupS2(img):
        return {
            'A': img.select('B1'),
            'B': img.select('B2'),
            'G': img.select('B3'),
            'R': img.select('B4'),
            'RE1': img.select('B5'),
            'RE2': img.select('B6'),
            'RE3': img.select('B7'),
            'N' : img.select('B8'),
            'RE4': img.select('B8A'),
            'WV' : img.select('B9'),            
            'S1': img.select('B11'),
            'S2': img.select('B12')
        }

    def lookupL8(img):
        return {
            'A': img.select('B1'),
            'B': img.select('B2'),
            'G': img.select('B3'),
            'R': img.select('B4'),
            'N': img.select('B5'),
            'S1': img.select('B6'),
            'S2': img.select('B7'),                
            'T1' : img.select('B10'),
            'T2': img.select('B11')
        }

    def lookupL457(img):
        return {
            'B': img.select('B1'),
            'G': img.select('B2'),
            'R': img.select('B3'),
            'N': img.select('B4'),
            'S1': img.select('B5'),
            'T1': img.select('B6'),
            'S2': img.select('B7')                
        }
    
    def lookupMOD09GQ(img):
        return {            
            'R': img.select('sur_refl_b01'),
            'N': img.select('sur_refl_b02')            
        }
    
    def lookupMOD09GA(img):
        return {            
            'B': img.select('sur_refl_b03'),
            'G': img.select('sur_refl_b04'),
            'R': img.select('sur_refl_b01'),
            'N': img.select('sur_refl_b02'),
            'S1': img.select('sur_refl_b06'),
            'S2': img.select('sur_refl_b07')           
        }
    
    def lookupMCD43A4(img):
        return {            
            'B': img.select('Nadir_Reflectance_Band3'),
            'G': img.select('Nadir_Reflectance_Band4'),
            'R': img.select('Nadir_Reflectance_Band1'),
            'N': img.select('Nadir_Reflectance_Band2'),
            'S1': img.select('Nadir_Reflectance_Band6'),
            'S2': img.select('Nadir_Reflectance_Band7')           
        }

    lookupPlatform = {
        'COPERNICUS/S2': lookupS2,
        'LANDSAT/LC08': lookupL8,
        'LANDSAT/LE07': lookupL457,
        'LANDSAT/LT05': lookupL457,
        'LANDSAT/LT04': lookupL457,
        'MODIS/006/MOD09GQ': lookupMOD09GQ,
        'MODIS/006/MYD09GQ': lookupMOD09GQ,
        'MODIS/006/MOD09GA': lookupMOD09GA,
        'MODIS/006/MYD09GA': lookupMOD09GA,
        'MODIS/006/MOD09Q1': lookupMOD09GQ,
        'MODIS/006/MYD09Q1': lookupMOD09GQ,
        'MODIS/006/MOD09A1': lookupMOD09GA,
        'MODIS/006/MYD09A1': lookupMOD09GA,
        'MODIS/006/MCD43A4': lookupMCD43A4
    }

    if platformDict['platform'] not in list(lookupPlatform.keys()):
        raise Exception("Sorry, satellite platform not supported for index computation!")

    return lookupPlatform[platformDict['platform']](img)

def _get_indices():
    '''Retrieves the dictionary of indices used for the index() method in ee.Image and ee.ImageCollection classes.
           
    Returns
    -------
    dict
        Indices.
    '''
    vegetationIndices = {
        'BNDVI' : {
            'formula' : '(N - B)/(N + B)',
            'description' : 'Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','B'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=135',
            'contributor' : 'davemlz'
        },
        'CIG' : {
            'formula' : '(N / G) - 1.0',
            'description' : 'Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','G'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=128',
            'contributor' : 'davemlz'
        },
        'CVI' : {
            'formula' : '(N * R) / (G ** 2.0)',
            'description' : 'Chlorophyll Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','R','G'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=391',
            'contributor' : 'davemlz'
        },
        'EVI' : {
            'formula' : 'g * (N - R) / (N + C1 * R - C2 * B + L)',
            'description' : 'Enhanced Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','g','R','C1','C2','B','L'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=16',
            'contributor' : 'davemlz'
        },
        'EVI2' : {
            'formula' : 'g * (N - R) / (N + 2.4 * R + L)',
            'description' : 'Two-Band Enhanced Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','g','R','L'],
            'reference' : 'https://doi.org/10.1016/j.rse.2008.06.006',
            'contributor' : 'davemlz'
        },
        'GARI' : {
            'formula' : '(N - (G - (B - R))) / (N - (G + (B - R)))',
            'description' : 'Green Atmospherically Resistant Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','G','B','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=363',
            'contributor' : 'davemlz'
        },
        'GBNDVI' : {
            'formula' : '(N - (G + B))/(N + (G + B))',
            'description' : 'Green-Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','B','G'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=186',
            'contributor' : 'davemlz'
        }, 
        'GEMI' : {
            'formula' : '((2.0*((N ** 2.0)-(R ** 2.0)) + 1.5*N + 0.5*R)/(N + R + 0.5))*(1.0 - 0.25*((2.0 * ((N ** 2.0) - (R ** 2)) + 1.5 * N + 0.5 * R)/(N + R + 0.5)))-((R - 0.125)/(1 - R))',
            'description' : 'Global Environment Monitoring Index',
            'type' : 'vegetation',
            'requires' : ['N','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=25',
            'contributor' : 'davemlz'
        },
        'GLI' : {
            'formula' : '(2.0 * G - R - B) / (2.0 * G + R + B)',
            'description' : 'Green Leaf Index',
            'type' : 'vegetation',
            'requires' : ['G','B','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=375',
            'contributor' : 'davemlz'
        },
        'GNDVI' : {
            'formula' : '(N - G)/(N + G)',
            'description' : 'Green Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','G'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=401',
            'contributor' : 'davemlz'
        },
        'GRNDVI' : {
            'formula' : '(N - (G + R))/(N + (G + R))',
            'description' : 'Green-Red Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','G','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=185',
            'contributor' : 'davemlz'
        },
        'GVMI' : {
            'formula' : '((N + 0.1) - (S2 + 0.02)) / ((N + 0.1) + (S2 + 0.02))',
            'description' : 'Global Vegetation Moisture Index',
            'type' : 'vegetation',
            'requires' : ['N','S2'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=372',
            'contributor' : 'davemlz'
        },
        'MNDVI' : {
            'formula' : '(N - S2)/(N + S2)',
            'description' : 'Modified Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','S2'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=245',
            'contributor' : 'davemlz'
        },  
        'NDVI' : {
            'formula' : '(N - R)/(N + R)',
            'description' : 'Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=58',
            'contributor' : 'davemlz'
        },  
        'NGRDI' : {
            'formula' : '(G - R) / (G + R)',
            'description' : 'Normalized Green Red Difference Index',
            'type' : 'vegetation',
            'requires' : ['G','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=390',
            'contributor' : 'davemlz'
        },  
        'RVI' : {
            'formula' : 'N / R',
            'description' : 'Ratio Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=72',
            'contributor' : 'davemlz'
        },
        'SAVI' : {
            'formula' : '(1.0 + L) * (N - R) / (N + R + L)',
            'description' : 'Soil-Adjusted Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','R','L'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=87',
            'contributor' : 'davemlz'
        },
        'VARI' : {
            'formula' : '(G - R) / (G + R - B)',
            'description' : 'Visible Atmospherically Resistant Index',
            'type' : 'vegetation',
            'requires' : ['G','R','B'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=356',
            'contributor' : 'davemlz'
        },
    }
    
    burnIndices = {
        'BAI' : {
            'formula' : '1.0 / ((0.1 - R) ** 2.0 + (0.06 - N) ** 2.0)',
            'description' : 'Burned Area Index',
            'type' : 'burn',
            'requires' : ['N','R'],
            'reference' : 'https://digital.csic.es/bitstream/10261/6426/1/Martin_Isabel_Serie_Geografica.pdf',
            'contributor' : 'davemlz'
        },        
        'BAIS2' : {
            'formula' : '(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5) * (((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)',
            'description' : 'Burned Area Index for Sentinel 2',
            'type' : 'burn',
            'requires' : ['RE2','RE3','RE4','R','S2'],
            'reference' : 'https://doi.org/10.3390/ecrs-2-05177',
            'contributor' : 'davemlz'
        },  
        'CSIT' : {
            'formula' : 'N / (S2 * T1 / 10000.0)',
            'description' : 'Char Soil Index Thermal',
            'type' : 'burn',
            'requires' : ['N','S2','T1'],
            'reference' : 'https://doi.org/10.1080/01431160600954704',
            'contributor' : 'davemlz'
        }, 
        'NBR' : {
            'formula' : '(N - S2) / (N + S2)',
            'description' : 'Normalized Burn Ratio',
            'type' : 'burn',
            'requires' : ['N','S2'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=53',
            'contributor' : 'davemlz'
        }, 
        'NBRT' : {
            'formula' : '(N - (S2 * T1 / 10000.0)) / (N + (S2 * T1 / 10000.0))',
            'description' : 'Normalized Burn Ratio Thermal',
            'type' : 'burn',
            'requires' : ['N','S2','T1'],
            'reference' : 'https://doi.org/10.1080/01431160500239008',
            'contributor' : 'davemlz'
        }, 
        'NDVIT' : {
            'formula' : '(N - (R * T1 / 10000.0))/(N + (R * T1 / 10000.0))',
            'description' : 'Normalized Difference Vegetation Index Thermal',
            'type' : 'burn',
            'requires' : ['N','R','T1'],
            'reference' : 'https://doi.org/10.1080/01431160600954704',
            'contributor' : 'davemlz'
        }, 
        'SAVIT' : {
            'formula' : '(1.0 + L) * (N - (R * T1 / 10000.0)) / (N + (R * T1 / 10000.0) + L)',
            'description' : 'Soil-Adjusted Vegetation Index Thermal',
            'type' : 'burn',
            'requires' : ['N','R','L','T1'],
            'reference' : 'https://doi.org/10.1080/01431160600954704',
            'contributor' : 'davemlz'
        },        
    }
    
    waterIndices = {
        'MNDWI' : {
            'formula' : '(G - S1) / (G + S1)',
            'description' : 'Modified Normalized Difference Water Index',
            'type' : 'water',
            'requires' : ['G','S1'],
            'reference' : 'https://doi.org/10.1080/01431160600589179',
            'contributor' : 'davemlz'
        },        
        'NDWI' : {
            'formula' : '(G - N) / (G + N)',
            'description' : 'Normalized Difference Water Index',
            'type' : 'water',
            'requires' : ['G','N'],
            'reference' : 'https://doi.org/10.1080/01431169608948714',
            'contributor' : 'davemlz'
        },   
    }
    
    snowIndices = {
        'NDSI' : {
            'formula' : '(G - S1) / (G + S1)',
            'description' : 'Normalized Difference Snow Index',
            'type' : 'snow',
            'requires' : ['G','S1'],
            'reference' : 'https://doi.org/10.1109/IGARSS.1994.399618',
            'contributor' : 'davemlz'
        },   
    }
    
    droughtIndices = {
        'NDDI' : {
            'formula' : '(((N - R)/(N + R)) - ((G - N)/(G + N)))/(((N - R)/(N + R)) + ((G - N)/(G + N)))',
            'description' : 'Normalized Difference Drought Index',
            'type' : 'drought',
            'requires' : ['N','R','G'],
            'reference' : 'https://doi.org/10.1029/2006GL029127',
            'contributor' : 'davemlz'
        },
    }
    
    kernelIndices = {
        'kEVI' : {
            'formula' : 'g * (kNN - kNR) / (kNN + C1 * kNR - C2 * kNB + kNL)',
            'description' : 'Kernel Enhanced Vegetation Index',
            'type' : 'kernel',
            'requires' : ['kNN','g','kNR','C1','C2','kNB','kNL'],
            'reference' : 'https://doi.org/10.1126/sciadv.abc7447',
            'contributor' : 'davemlz'
        },
        'kNDVI' : {
            'formula' : '(kNN - kNR)/(kNN + kNR)',
            'description' : 'Kernel Normalized Difference Vegetation Index',
            'type' : 'kernel',
            'requires' : ['kNN','kNR'],
            'reference' : 'https://doi.org/10.1126/sciadv.abc7447',
            'contributor' : 'davemlz'
        },
        'kRVI' : {
            'formula' : 'kNN / kNR',
            'description' : 'Kernel Ratio Vegetation Index',
            'type' : 'kernel',
            'requires' : ['kNN','kNR'],
            'reference' : 'https://doi.org/10.1126/sciadv.abc7447',
            'contributor' : 'davemlz'
        },
        'kVARI' : {
            'formula' : '(kGG - kGR) / (kGG + kGR - kGB)',
            'description' : 'Kernel Visible Atmospherically Resistant Index',
            'type' : 'kernel',
            'requires' : ['kGG','kGR','kGB'],
            'reference' : 'https://doi.org/10.1126/sciadv.abc7447',
            'contributor' : 'davemlz'
        },
    }
    
    indices = {**vegetationIndices, **burnIndices, **waterIndices, **snowIndices, **droughtIndices, **kernelIndices}
    
    return indices

def _get_kernel_image(img,lookup,kernel,sigma,a,b):
    '''Creates an ee.Image representing a kernel computed on bands [a] and [b].
    
    Parameters
    ----------    
    img : ee.Image
        Image to compute the kernel on.       
    lookup : dict
        Dictionary retrieved from _get_expression_map().
    kernel : str
        Kernel to use.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'.
    a : str
        Key of the first band to use.
    b : str
        Key of the second band to use.
        
    Returns
    -------
    ee.Image
        Kernel image.
    '''
    if a not in list(lookup.keys()) or b not in list(lookup.keys()):
        return None
    else:    
        lookupab = {
            'a': lookup[a],
            'b': lookup[b]
        }
        if isinstance(sigma,str):
            lookup = {**lookup, **lookupab, 'sigma': img.expression(sigma,lookupab)}
        else:
            lookup = {**lookup, **lookupab, 'sigma': sigma}        
        kernels = {
            'linear' : 'a * b',
            'RBF': 'exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))',
            'poly': '((a * b) + c) ** p',
        }
        return img.expression(kernels[kernel],lookup)

def _remove_none_dict(dictionary):
    '''Removes elements from a dictionary with None values.
    
    Parameters
    ----------    
    dictionary : dict
        
    Returns
    -------
    dict
        Curated dictionary.
    '''
    newDictionary = dict(dictionary)
    for key in dictionary.keys():
        if dictionary[key] is None:
            del newDictionary[key]
    return newDictionary    

def _get_kernel_parameters(img,lookup,kernel,sigma):
    '''Gets the additional kernel parameters to compute kernel indices.
    
    Parameters
    ----------    
    img : ee.Image
        Image to compute the kernel parameters on.       
    lookup : dict
        Dictionary retrieved from _get_expression_map().
    kernel : str
        Kernel to use.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'.
        
    Returns
    -------
    dict
        Kernel parameters.
    '''
    kernelParameters = {
        'kNN' : _get_kernel_image(img,lookup,kernel,sigma,'N','N'),
        'kNR' : _get_kernel_image(img,lookup,kernel,sigma,'N','R'),
        'kNB' : _get_kernel_image(img,lookup,kernel,sigma,'N','B'),
        'kNL' : _get_kernel_image(img,lookup,kernel,sigma,'N','L'),
        'kGG' : _get_kernel_image(img,lookup,kernel,sigma,'G','G'),
        'kGR' : _get_kernel_image(img,lookup,kernel,sigma,'G','R'),
        'kGB' : _get_kernel_image(img,lookup,kernel,sigma,'G','B'),
    }

    return kernelParameters

def _index(self,index,G,C1,C2,L,kernel,sigma,p,c):
    '''Computes one or more spectral indices (indices are added as bands) for an image oir image collection.
    
    Parameters
    ----------    
    self : ee.Image | ee.ImageCollection
        Image to compute indices on. Must be scaled to [0,1]. Check the supported platforms in User Guide > Spectral Indices > Supported Platforms.        
    index : string | list[string]
        Index or list of indices to compute.
    G : float
        Gain factor. Used just for index = 'EVI'. 
    C1 : float
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
    kernel : str
        Kernel used for kernel indices.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'. If str, this must be an expression including 'a' and 'b'. If numeric, this must be positive.
    p : float
        Kernel degree. Used for kernel = 'poly'.
    c : float
        Free parameter that trades off the influence of higher-order versus lower-order terms. Used for kernel = 'poly'. This must be greater than or equal to 0.
            
    Returns
    -------
    ee.Image | ee.ImageCollection
        Image (or Image Collection) with the computed spectral index, or indices, as new bands.
    '''
    platformDict = _get_platform(self)
    
    if isinstance(sigma,int) or isinstance(sigma,float):
        if sigma < 0:
            raise Exception('[sigma] must be positive!')
    
    if p <= 0 or c < 0:
        raise Exception('[p] and [c] must be positive!')
    
    additionalParameters = {
        'g': float(G),
        'C1': float(C1),
        'C2': float(C2),
        'L': float(L),
        'p': float(p),
        'c': float(c)
    }
    
    spectralIndices = _get_indices()
    indicesNames = list(spectralIndices.keys())
        
    if not isinstance(index, list):
        if index == 'all':
            index = list(spectralIndices.keys())
        elif index in ['vegetation','burn','water','snow','drought','kernel']:
            temporalListOfIndices = []
            for idx in indicesNames:
                if spectralIndices[idx]['type'] == index:
                    temporalListOfIndices.append(idx)
            index = temporalListOfIndices
        else:
            index = [index]        
            
    for idx in index:
        if idx not in list(spectralIndices.keys()):
            warnings.warn("Index " + idx + " is not a built-in index and it won't be computed!",Warning)
        else:
            def temporalIndex(img):
                lookupDic = _get_expression_map(img, platformDict)
                lookupDic = {**lookupDic, **additionalParameters}
                kernelParameters = _get_kernel_parameters(img,lookupDic,kernel,sigma)
                lookupDic = {**lookupDic, **kernelParameters}
                lookupDicCurated = _remove_none_dict(lookupDic)
                if all(band in list(lookupDicCurated.keys()) for band in spectralIndices[idx]['requires']):
                    return img.addBands(img.expression(spectralIndices[idx]['formula'],lookupDicCurated).rename(idx))                
                else:
                    warnings.warn("This platform doesn't have the required bands for " + idx + " computation!",Warning)
                    return img
            if isinstance(self,ee.imagecollection.ImageCollection):
                self = self.map(temporalIndex)
            elif isinstance(self,ee.image.Image):
                self = temporalIndex(self)
            
    return self

def indices():
    '''Gets the dictionary of available indices as a Box object.
        
    Returns
    -------
    Box
        Dictionary of available indices. For each index, the keys 'description', 'formula', 'requires', 'reference' and 'contributor' can be checked.
        
    Examples
    --------
    >>> import eemont
    >>> indices = eemont.indices()
    >>> indices.BAIS2.description
    'Burned Area Index for Sentinel 2'
    >>> indices.BAIS2.formula
    '(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5) * (((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)'
    >>> indices.BAIS2.reference
    'https://doi.org/10.3390/ecrs-2-05177'
    '''
    return Box(_get_indices(),frozen_box = True)

def listIndices():
    '''Gets the list of available indices.
        
    Returns
    -------
    list
        List of available indices.
        
    Examples
    --------
    >>> import eemont
    >>> eemont.listIndices()
    ['BNDVI','CIG','CVI','EVI','EVI2','GBNDVI','GNDVI',...]
    '''
    return list(_get_indices().keys())

def _get_platform(args):
    '''Gets the platform (satellite) of an image (or image collection) and wheter if it is a Surface Reflectance product.
    
    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image to get platform.
        
    Returns
    -------
    dict
        Platform and product of the image (or image collection).
    '''
    platforms = [
        'COPERNICUS/S3',
        'COPERNICUS/S2',
        'LANDSAT/LC08',
        'LANDSAT/LE07',
        'LANDSAT/LT05',
        'LANDSAT/LT04',
        'MODIS/006/MCD43A4',
        'MODIS/006/MCD43A3',
        'MODIS/006/MOD09GQ',
        'MODIS/006/MOD10A1',
        'MODIS/006/MOD11A1',
        'MODIS/006/MOD09GA',
        'MODIS/006/MODOCGA',
        'MODIS/006/MOD14A1',
        'MODIS/006/MCD43A1',
        'MODIS/006/MCD15A3H',
        'MODIS/006/MOD09Q1',
        'MODIS/006/MOD09A1',
        'MODIS/006/MOD11A2',
        'MODIS/006/MOD17A2H',
        'MODIS/006/MOD16A2',
        'MODIS/006/MOD13Q1',
        'MODIS/006/MOD13A1',
        'MODIS/006/MOD13A2',
        'MODIS/061/MOD08_M3',
        'MODIS/006/MOD17A3HGF',
        'MODIS/006/MYD09GQ',
        'MODIS/006/MYD10A1',
        'MODIS/006/MYD11A1',
        'MODIS/006/MYD09GA',
        'MODIS/006/MYDOCGA',
        'MODIS/006/MYD14A1',        
        'MODIS/006/MYD09Q1',
        'MODIS/006/MYD09A1',
        'MODIS/006/MYD11A2',
        'MODIS/006/MYD17A2H',        
        'MODIS/006/MYD13Q1',
        'MODIS/006/MYD13A1',
        'MODIS/006/MYD13A2',
        'MODIS/061/MYD08_M3',
        'MODIS/006/MYD17A3HGF'
    ]
    
    if isinstance(args, ee.imagecollection.ImageCollection):
        imgID = args.first().get('system:id').getInfo()
    elif isinstance(args, ee.image.Image):
        imgID = args.get('system:id').getInfo()
    else:
        raise Exception("Sorry, just ee.Image or ee.ImageCollection classes supported!")
    
    plt = None
    
    for platform in platforms:
        if platform in imgID:
            plt = platform
        if '_SR' in imgID:
            platformDict = {'platform': plt, 'sr': True}
        else:
            platformDict = {'platform': plt, 'sr': False}
            
    if plt is None:
        raise Exception("Sorry, satellite platform not supported!")
            
    return platformDict

def _get_scale_method(platformDict):
    '''Gets the scale algorithms for the scale() method in ee.Imge and ee.ImageCollection.
    
    Parameters
    ----------
    platformDict : dict
        Dictionary retrieved from the _get_platform() method.
        
    Returns
    -------
    dict
        Lookup dictionary for scale algorithms.
    '''    
    def S3(img):
        scalars = [
            0.0139465,
            0.0133873,
            0.0121481,
            0.0115198,
            0.0100953,
            0.0123538,
            0.00879161,
            0.00876539,
            0.0095103,
            0.00773378,
            0.00675523,
            0.0071996,
            0.00749684,
            0.0086512,
            0.00526779,
            0.00530267,
            0.00493004,
            0.00549962,
            0.00502847,
            0.00326378,
            0.00324118
        ]
        scaled = img.select(['Oa.*']).multiply(scalars).addBands(img.select('quality_flags'))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def S2(img):
        scaled = img.select(['B.*']).divide(1e4)      
        scaled = scaled.addBands(img.select(['Q.*']))
        if platformDict['sr']:            
            scaled = scaled.addBands(img.select(['AOT','WVP']).divide(1e3))
            scaled = scaled.addBands(img.select(['T.*']))            
            scaled = scaled.addBands(img.select('SCL'))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def L8(img):               
        if platformDict['sr']:
            scaled = img.select(['B[1-9]']).divide(1e4)
            scaled = scaled.addBands(img.select(['B10','B11']).divide(10)) 
            scaled = scaled.addBands(img.select(['sr_aerosol','pixel_qa','radsat_qa']))
            return ee.Image(scaled.copyProperties(img,img.propertyNames()))
        else:
            warnings.warn("TOA reflectance for Landsat 8 is already scaled!",Warning)
            pass
        
    def L457(img):               
        if platformDict['sr']:
            scaled = img.select(['B[1-5]','B7']).divide(1e4)
            scaled = scaled.addBands(img.select(['B6']).divide(10)) 
            scaled = scaled.addBands(img.select(['sr_atmos_opacity']).divide(1e3)) 
            scaled = scaled.addBands(img.select(['sr_cloud_qa','pixel_qa','radsat_qa']))
            return ee.Image(scaled.copyProperties(img,img.propertyNames()))
        else:
            warnings.warn("TOA reflectance for Landsat 4, 5 and 7 is already scaled!",Warning)
            pass
    
    def MCD43A4(img):
        scaled = img.select(['Nadir.*']).divide(1e4)      
        scaled = scaled.addBands(img.select(['BRDF.*']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MCD43A3(img):
        scaled = img.select(['Albedo.*']).divide(1e3)      
        scaled = scaled.addBands(img.select(['BRDF.*']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD09GQ(img):
        scaled = img.select(['sur.*']).divide(1e4)
        scaled = scaled.addBands(img.select(['obscov']).divide(100)) 
        scaled = scaled.addBands(img.select(['num_observations','QC_250m','iobs_res','orbit_pnt','granule_pnt']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD10A1(img):
        scaled = img.select(['NDSI']).divide(1e4)      
        scaled = scaled.addBands(img.select(['NDSI_Snow.*']))
        scaled = scaled.addBands(img.select(['Snow.*']))
        scaled = scaled.addBands(img.select(['orbit_pnt','granule_pnt']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD11A1(img):
        scaled = img.select(['LST.*']).multiply(0.02)
        scaled = scaled.addBands(img.select(['Day_view_time','Night_view_time']).multiply(0.1)) 
        scaled = scaled.addBands(img.select(['Emis.*']).multiply(0.002)) 
        scaled = scaled.addBands(img.select(['Clear.*']).multiply(0.0005))
        scaled = scaled.addBands(img.select(['QC_Day','Day_view_angle','QC_Night','Night_view_angle']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD09GA(img):
        scaled = img.select(['sur.*']).multiply(0.0001)        
        scaled = scaled.addBands(img.select(['Sensor.*']).multiply(0.01)) 
        scaled = scaled.addBands(img.select(['Solar.*']).multiply(0.01)) 
        scaled = scaled.addBands(img.select(['Range']).multiply(25))
        scaled = scaled.addBands(img.select(['num_observations_1km','state_1km','gflags','orbit_pnt','granule_pnt','num_observations_500m','QC_500m','obscov_500m','iobs_res','q_scan']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MODOCGA(img):
        scaled = img.select(['sur.*']).multiply(0.0001)  
        scaled = scaled.addBands(img.select(['num_observations','orbit_pnt','granule_pnt']))
        scaled = scaled.addBands(img.select(['QC.*']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD14A1(img):
        scaled = img.select(['MaxFRP']).multiply(0.1)  
        scaled = scaled.addBands(img.select(['FireMask','sample','QA']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MCD43A1(img):
        scaled = img.select(['BRDF_Albedo_Parameters.*']).multiply(0.001)  
        scaled = scaled.addBands(img.select(['BRDF_Albedo_Band.*']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MCD15A3H(img):
        scaled = img.select(['Fpar','FparStdDev']).multiply(0.01)  
        scaled = scaled.addBands(img.select(['Lai','LaiStdDev']).multiply(0.1)) 
        scaled = scaled.addBands(img.select(['FparLai_QC','FparExtra_QC']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD09Q1(img):
        scaled = img.select(['sur.*']).divide(1e4)        
        scaled = scaled.addBands(img.select(['State','QA']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD09A1(img):
        scaled = img.select(['sur.*']).divide(1e4)
        scaled = scaled.addBands(img.select(['SolarZenith','ViewZenith','RelativeAzimuth']).multiply(0.01)) 
        scaled = scaled.addBands(img.select(['QA','StateQA','DayOfYear']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD11A2(img):
        scaled = img.select(['LST.*']).multiply(0.02)
        scaled = scaled.addBands(img.select(['Day_view_time','Night_view_time']).multiply(0.1)) 
        scaled = scaled.addBands(img.select(['Emis.*']).multiply(0.002).add(0.49)) 
        scaled = scaled.addBands(img.select(['Day_view_angl','Night_view_angl']).subtract(65))
        scaled = scaled.addBands(img.select(['QC_Day','QC_Night','Clear_sky_days','Clear_sky_nights']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD17A2H(img):
        scaled = img.select(['Gpp','PsnNet']).multiply(0.0001)
        scaled = scaled.addBands(img.select(['Psn_QC']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD16A2(img):
        scaled = img.select(['ET','PET']).multiply(0.1)
        scaled = scaled.addBands(img.select(['LE','PLE']).multiply(0.0001))
        scaled = scaled.addBands(img.select(['ET_QC']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD13Q1(img):
        scaled = img.select(['NDVI','EVI']).multiply(0.0001)
        scaled = scaled.addBands(img.select(['sur.*']).multiply(0.0001))
        scaled = scaled.addBands(img.select(['ViewZenith','SolarZenith','RelativeAzimuth']).multiply(0.01))
        scaled = scaled.addBands(img.select(['DetailedQA','DayOfYear','SummaryQA']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD13A1(img):
        scaled = img.select(['NDVI','EVI']).multiply(0.0001)
        scaled = scaled.addBands(img.select(['sur.*']).multiply(0.0001))
        scaled = scaled.addBands(img.select(['ViewZenith','SolarZenith','RelativeAzimuth']).multiply(0.01))
        scaled = scaled.addBands(img.select(['DetailedQA','DayOfYear','SummaryQA']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD13A2(img):
        scaled = img.select(['NDVI','EVI']).multiply(0.0001)
        scaled = scaled.addBands(img.select(['sur.*']).multiply(0.0001))
        scaled = scaled.addBands(img.select(['ViewZenith','SolarZenith','RelativeAzimuth']).multiply(0.01))
        scaled = scaled.addBands(img.select(['DetailedQA','DayOfYear','SummaryQA']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD08_M3(img):
        scaled = img.select(['Aerosol.*']).multiply(0.001)
        scaled = scaled.addBands(img.select(['Cirrus.*']).multiply(0.0001))
        scaled = scaled.addBands(img.select(['Cloud_Optical_Thickness_Liquid_Log.*']).multiply(0.001))
        scaled = scaled.addBands(img.select(['Cloud_Optical_Thickness_Liquid_Mean_Uncertainty']).multiply(0.01))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def MOD17A3HGF(img):
        scaled = img.select(['Npp']).multiply(0.0001)
        scaled = scaled.addBands(img.select(['Npp_QC']))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    lookup = {
        'COPERNICUS/S3': S3,
        'COPERNICUS/S2': S2,
        'LANDSAT/LC08': L8,
        'LANDSAT/LE07': L457,
        'LANDSAT/LT05': L457,
        'LANDSAT/LT04': L457,
        'MODIS/006/MCD43A4': MCD43A4,
        'MODIS/006/MCD43A3': MCD43A3,
        'MODIS/006/MOD09GQ': MOD09GQ,
        'MODIS/006/MOD10A1': MOD10A1,
        'MODIS/006/MOD11A1': MOD11A1,
        'MODIS/006/MOD09GA': MOD09GA,
        'MODIS/006/MODOCGA': MODOCGA,
        'MODIS/006/MOD14A1': MOD14A1,
        'MODIS/006/MCD43A1': MCD43A1,
        'MODIS/006/MCD15A3H': MCD15A3H,
        'MODIS/006/MOD09Q1': MOD09Q1,
        'MODIS/006/MOD09A1': MOD09A1,
        'MODIS/006/MOD11A2': MOD11A2,
        'MODIS/006/MOD17A2H': MOD17A2H,
        'MODIS/006/MOD16A2': MOD16A2,
        'MODIS/006/MOD13Q1': MOD13Q1,
        'MODIS/006/MOD13A1': MOD13A1,
        'MODIS/006/MOD13A2': MOD13A2,
        'MODIS/061/MOD08_M3': MOD08_M3,
        'MODIS/006/MOD17A3HGF': MOD17A3HGF,       
        'MODIS/006/MYD09GQ': MOD09GQ,
        'MODIS/006/MYD10A1': MOD10A1,
        'MODIS/006/MYD11A1': MOD11A1,
        'MODIS/006/MYD09GA': MOD09GA,
        'MODIS/006/MYDOCGA': MODOCGA,
        'MODIS/006/MYD14A1': MOD14A1,        
        'MODIS/006/MYD09Q1': MOD09Q1,
        'MODIS/006/MYD09A1': MOD09A1,
        'MODIS/006/MYD11A2': MOD11A2,
        'MODIS/006/MYD17A2H': MOD17A2H,        
        'MODIS/006/MYD13Q1': MOD13Q1,
        'MODIS/006/MYD13A1': MOD13A1,
        'MODIS/006/MYD13A2': MOD13A2,
        'MODIS/061/MYD08_M3': MOD08_M3,
        'MODIS/006/MYD17A3HGF': MOD17A3HGF
    }
    
    return lookup