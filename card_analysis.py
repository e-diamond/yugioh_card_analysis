from json_handling import *
from cardsets import Set
import numpy as np
import matplotlib.pyplot as plt


cardsets_filename = "cardsets.json"
cards_filename = "cardinfo.json"

def updateLocalFiles():
    JSON.url2File("https://db.ygoprodeck.com/api/v7/cardsets.php", cardsets_filename)
    JSON.url2File("https://db.ygoprodeck.com/api/v7/cardinfo.php", cards_filename)

# find the index of the first set each card is printed in
def getFirstSet(sets_printed):

    # list of set names for all sets card printed in
    print_names = [printset["set_name"] for printset in sets_printed]

    # search cardsets for a printed set
    for i, set in enumerate(cardsets):
        if set.name in print_names:
            # return index of first set found
            return i

    # return none if set not found (no tcg release)
    return None

# calculates average name length for each set
def avNameLength():

    for card in cards:

        # get index of first print set in cardsets
        index = getFirstSet(card["card_sets"])

        # update set object
        if index != None:
            cardsets[index].update(len(card["name"]))

    # exclude reprint only sets
    new_card_sets = [set for set in cardsets if (not set.isReprintOnly())]

    # return averages
    return [set.getAverageLength() for set in new_card_sets]

"""START"""
# ask if user wants to update storage files
update = input("Would you like to update storage files? (y/n) ")

# update storage files
if update == "y" or update == "Y":
    updateLocalFiles()

# read data from local files
cardsets = JSON.readFromFile(cardsets_filename)
cards = JSON.readFromFile(cards_filename)["data"]

# remove sets with no tcg release date
cardsets = [set for set in cardsets if "tcg_date" in set]

# sort cardsets by date
cardsets.sort(key=lambda set: set["tcg_date"])

# change cardsets to object array
cardsets = [Set(set["set_name"], set["tcg_date"]) for set in cardsets]

# remove cards with no release set and remove tokens
cards = [card for card in cards if ("card_sets" in card and card["type"] != "Token")]

# get variable arrays
averages = avNameLength()
dates = [set.tcg_date for set in cardsets if (not set.isReprintOnly())]

def plotData(x, y, xlabel, ylabel, trendline=False):

    if trendline:
        x_deltas = [(xdata - x[0]).days for xdata in x]
        a, b = np.polyfit(x_deltas, y, 1)
        print("Rate of increase (days): ", a)
        plt.plot(x, a*np.array(x_deltas) + b, "r")

    plt.scatter(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

plotData(dates, averages, "Sets", "Mean length of card name (characters)", True)
