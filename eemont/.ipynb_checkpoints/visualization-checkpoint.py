def rgb(platform = 'S2',minValue = 0,maxValue = 0.3,scaled = True):
    
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