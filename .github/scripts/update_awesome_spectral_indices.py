import requests
import json
# Request Awesome List of Spectral Indices
awesomeSpectralIndices = requests.get('https://raw.githubusercontent.com/davemlz/awesome-ee-spectral-indices/main/output/spectral-indices-dict.json').json()
# Save the dict as json file
with open('./eemont/data/spectral-indices-dict.json','w') as fp:
    json.dump(awesomeSpectralIndices, fp, indent = 4, sort_keys = True)