import ee

def _get_expression_map(img, platformDict):
    '''Gets the dictionary required for the map parameter in ee.Image.expression.
    
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

    lookupPlatform = {
        'COPERNICUS/S2': lookupS2,
        'LANDSAT/LC08': lookupL8,
        'LANDSAT/LE07': lookupL457,
        'LANDSAT/LT05': lookupL457,
        'LANDSAT/LT04': lookupL457
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
        'GBNDVI' : {
            'formula' : '(N - (G + B))/(N + (G + B))',
            'description' : 'Green-Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'requires' : ['N','B','G'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=186',
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
        'NBR' : {
            'formula' : '(N - S2) / (N + S2)',
            'description' : 'Normalized Burn Ratio',
            'type' : 'burn',
            'requires' : ['N','S2'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=53',
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
    
    indices = {**vegetationIndices, **burnIndices, **waterIndices, **snowIndices}
    
    return indices

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
        'MODIS/006/MOD17A3HGF'
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
        'MODIS/006/MOD17A3HGF': MOD17A3HGF
    }
    
    return lookup