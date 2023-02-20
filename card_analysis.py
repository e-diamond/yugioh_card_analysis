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

def plotData(x, y, title, xlabel, ylabel, trendline=False, weights=None):

    if trendline:

        if weights == None:
            weights = np.ones_like(y)

        x_deltas = [(xdata - x[0]).days for xdata in x]
        a, b = np.polyfit(x_deltas, y, 1, w=weights)
        print("Rate of increase (days): ", a)
        plt.plot(x, a*np.array(x_deltas) + b, "r")

    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


"""START"""
if __name__ == "__main__":

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
    Set.initialise(cardsets, cards, noeffect)

    # get variable arrays
    name_av = [set.averageNameLength() for set in Set.sets]
    desc_av = [set.averageDescLength() for set in Set.sets if (not set.isNonEffectOnly())]
    dates = [set.tcg_date for set in Set.sets]
    eff_dates = [set.tcg_date for set in Set.sets if (not set.isNonEffectOnly())]

    plotData(dates, name_av, "Average length of card names based on set release dates", "Sets", "Mean length of card name (characters)", trendline=True, weights=Set.getNameWeights())
    plotData(eff_dates, desc_av, "Average length of card effect text based on set release dates", "Sets", "Mean length of effect text (characters)")
