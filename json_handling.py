import json

def readJSONfromurl(url):
    import requests

    # ping url 
    response = requests.get(url)

    return json.loads(response.text)
