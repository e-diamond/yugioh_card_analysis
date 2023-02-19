from json_handling import *
from cardsets import Set
import numpy as np
import matplotlib.pyplot as plt


cardsets_filename = "cardsets.json"
cards_filename = "cardinfo.json"
noeffect_filename = "noeffect.json"

def updateLocalFiles():
    JSON.url2File("https://db.ygoprodeck.com/api/v7/cardsets.php", cardsets_filename)
    JSON.url2File("https://db.ygoprodeck.com/api/v7/cardinfo.php", cards_filename)
    JSON.url2File("https://db.ygoprodeck.com/api/v7/cardinfo.php?has_effect=false", noeffect_filename)

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


"""START"""
# ask if user wants to update storage files
update = input("Would you like to update storage files? (y/n) ")

# update storage files
if update == "y" or update == "Y":
    updateLocalFiles()

# read data from local files
cardsets = JSON.readFromFile(cardsets_filename)
cards = JSON.readFromFile(cards_filename)["data"]

# only require names of effectless cards
noeffect = JSON.readFromFile(noeffect_filename)["data"]
noeffect = [card["name"] for card in noeffect]

# initialise set objects
cardsets = Set.initialise(cardsets, cards, noeffect)

# get variable arrays
name_av = [set.averageNameLength() for set in cardsets if (not set.isReprintOnly())]
desc_av = [set.averageDescLength() for set in cardsets if (not set.isReprintOnly() and not set.isNonEffectOnly())]
dates = [set.tcg_date for set in cardsets if (not set.isReprintOnly())]
eff_dates = [set.tcg_date for set in cardsets if (not set.isReprintOnly() and not set.isNonEffectOnly())]


plotData(dates, name_av, "Sets", "Mean length of card name (characters)", True)
plotData(eff_dates, desc_av, "Sets", "Mean length of description (characters)")
