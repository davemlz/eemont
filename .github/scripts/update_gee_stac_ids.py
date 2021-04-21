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
            dataset = requests.get(dataset['href']).json()
            if dataset['gee:type'] in ['image','image_collection']:
                eeDict[dataset['id']] = dataset['gee:type']
# Save the list as a json file
with open('./eemont/data/ee-catalog-ids.json','w') as fp:
    json.dump(eeDict, fp, indent = 4, sort_keys = True)