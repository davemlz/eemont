def _getIndices():
    """Retrieves the dictionary of indices used for the index() method in ee.Image and ee.ImageCollection classes."""
    
    vegetationIndices = {
        'BNDVI' : {
            'formula' : '(N - B)/(N + B)',
            'description' : 'Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=135',
            'contributor' : 'davemlz'
        },
        'CIG' : {
            'formula' : '(N / G) - 1.0',
            'description' : 'Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=128',
            'contributor' : 'davemlz'
        },
        'CVI' : {
            'formula' : '(N * R) / (G ** 2)',
            'description' : 'Chlorophyll Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=391',
            'contributor' : 'davemlz'
        },
        'EVI' : {
            'formula' : 'G * (N - R) / (N + C1 * R - C2 * B + L)',
            'description' : 'Enhanced Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=16',
            'contributor' : 'davemlz'
        },  
        'GBNDVI' : {
            'formula' : '(N - (G + B))/(N + (G + B))',
            'description' : 'Green-Blue Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=186',
            'contributor' : 'davemlz'
        }, 
        'GNDVI' : {
            'formula' : '(N - G)/(N + G)',
            'description' : 'Green Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=401',
            'contributor' : 'davemlz'
        },
        'GRNDVI' : {
            'formula' : '(N - (G + R))/(N + (G + R))',
            'description' : 'Green-Red Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=185',
            'contributor' : 'davemlz'
        }, 
        'MNDVI' : {
            'formula' : '(N - S2)/(N + S2)',
            'description' : 'Modified Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=245',
            'contributor' : 'davemlz'
        },  
        'NDVI' : {
            'formula' : '(N - R)/(N + R)',
            'description' : 'Normalized Difference Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=58',
            'contributor' : 'davemlz'
        },  
        'NGRDI' : {
            'formula' : '(G - R) / (G + R)',
            'description' : 'Normalized Green Red Difference Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=390',
            'contributor' : 'davemlz'
        },  
        'RVI' : {
            'formula' : 'N / R',
            'description' : 'Ratio Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=72',
            'contributor' : 'davemlz'
        },
        'SAVI' : {
            'formula' : '(1 + L) * (N - R) / (N + R + L)',
            'description' : 'Soil-Adjusted Vegetation Index',
            'type' : 'vegetation',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=87',
            'contributor' : 'davemlz'
        },          
    }
    
    burnIndices = {
        'BAI' : {
            'formula' : '1.0 / ((0.1 - R) ** 2.0 + (0.06 - N) ** 2.0)',
            'description' : 'Burned Area Index',
            'type' : 'burn',
            'reference' : 'https://digital.csic.es/bitstream/10261/6426/1/Martin_Isabel_Serie_Geografica.pdf',
            'contributor' : 'davemlz'
        },        
        'BAIS2' : {
            'formula' : '(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5) * (((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)',
            'description' : 'Burned Area Index for Sentinel 2',
            'type' : 'burn',
            'reference' : 'https://doi.org/10.3390/ecrs-2-05177',
            'contributor' : 'davemlz'
        },  
        'NBR' : {
            'formula' : '(N - S2) / (N + S2)',
            'description' : 'Normalized Burn Ratio',
            'type' : 'burn',
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=53',
            'contributor' : 'davemlz'
        }, 
    }
    
    waterIndices = {
        'MNDWI' : {
            'formula' : '(G - S1) / (G + S1)',
            'description' : 'Modified Normalized Difference Water Index',
            'type' : 'water',
            'reference' : 'https://doi.org/10.1080/01431160600589179',
            'contributor' : 'davemlz'
        },        
        'NDWI' : {
            'formula' : '(G - N) / (G + N)',
            'description' : 'Normalized Difference Water Index',
            'type' : 'water',
            'reference' : 'https://doi.org/10.1080/01431169608948714',
            'contributor' : 'davemlz'
        },    
    }
    
    snowIndices = {
        'NDSI' : {
            'formula' : '(G - S1) / (G + S1)',
            'description' : 'Normalized Difference Snow Index',
            'type' : 'snow',
            'reference' : 'https://doi.org/10.1109/IGARSS.1994.399618',
            'contributor' : 'davemlz'
        },   
    }
    
    indices = {**vegetationIndices, **burnIndices, **waterIndices, **snowIndices}
    
    return indices