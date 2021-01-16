from json_handling import readJSONfromurl

# get data from api
cardsets = readJSONfromurl("https://db.ygoprodeck.com/api/v7/cardsets.php")
cards = readJSONfromurl("https://db.ygoprodeck.com/api/v7/cardinfo.php")["data"]
