import json

class JSON:

    @staticmethod
    def readFromURL(url):
        import requests

        print("Downloading data...")
        response = requests.get(url)
        return json.loads(response.text)

    @staticmethod
    def readFromFile(filename):

        file = open(filename, "r")
        data = file.read()
        file.close()
        
        return json.loads(data)


    @classmethod
    def url2File(cls, url, filename):
        data = cls.readFromURL(url)

        print("Writing to file ", filename, "...")
        file = open(filename, "w")
        json.dump(data, file)
        file.close()
