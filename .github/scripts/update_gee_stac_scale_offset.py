import requests
import json
# Request ee scale offset catalog
eeCatalogScaleOffset = requests.get('https://raw.githubusercontent.com/davemlz/ee-catalog-scale-offset-params/main/list/ee-catalog-scale-offset-parameters.json').json()
# Get the datasets
eeScaleDict = dict()
eeOffsetDict = dict()
datasets = list(eeCatalogScaleOffset.keys())
for dataset in datasets:
    datasetScaleDict = dict()
    datasetOffsetDict = dict()
    bands = list(eeCatalogScaleOffset[dataset].keys())
    for band in bands:
        datasetScaleDict[band] = eeCatalogScaleOffset[dataset][band]['scale']
        datasetOffsetDict[band] = eeCatalogScaleOffset[dataset][band]['offset']
    eeScaleDict[dataset] = datasetScaleDict
    eeOffsetDict[dataset] = datasetOffsetDict
# Save the dicts as json files
with open('./eemont/data/ee-catalog-scale.json','w') as fp:
    json.dump(eeScaleDict, fp, indent = 4, sort_keys = True)
with open('./eemont/data/ee-catalog-offset.json','w') as fp:
    json.dump(eeOffsetDict, fp, indent = 4, sort_keys = True)