import requests
import json
# Request ee catalog
eeCatalog = requests.get('https://earthengine-stac.storage.googleapis.com/catalog/catalog.json').json()
# Get the datasets
eeDict = dict()
for dataset in eeCatalog['links']:
    if dataset['rel'] == 'child':
        response = requests.get(dataset['href'])
        if response.status_code == 200:
            datasetResponse = requests.get(dataset['href']).json()
            datasetDict = dict()
            if datasetResponse['gee:type'] in ['image','image_collection']:
                datasetDict['gee:type'] = datasetResponse['gee:type']      
                datasetDict['href'] = dataset['href']
                if 'sci:doi' in datasetResponse.keys():
                    datasetDict['sci:doi'] = datasetResponse['sci:doi']
                else:
                    datasetDict['sci:doi'] = 'DOI not available'
                if 'sci:citation' in datasetResponse.keys():
                    datasetDict['sci:citation'] = datasetResponse['sci:citation']
                else:
                    datasetDict['sci:citation'] = 'Citation not available'                
                eeDict[datasetResponse['id']] = datasetDict
# Save the list as a json file
with open('./eemont/data/ee-catalog-ids.json','w') as fp:
    json.dump(eeDict, fp, indent = 4, sort_keys = True)