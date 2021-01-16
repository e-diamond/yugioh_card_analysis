import json

def readJSONfromurl(url):
    import requests

    # ping url
    response = requests.get(url)

    return json.loads(response.text)


def readJSONfromfile(filename):

    # open and read file
    file = open(filename, "r")
    data = file.read()
    file.close()

    return json.loads(data)
