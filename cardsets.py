from datetime import date

class Set:

    def __init__(self, name, tcg_date):
        self.name = name
        self.tcg_date = date.fromisoformat(tcg_date)
        self.card_count = 0
        self.effect_count = 0
        self.name_rt = 0
        self.desc_rt = 0

    def update(self, name_length, desc_length=None):
        self.card_count = self.card_count + 1
        self.name_rt = self.name_rt + name_length

        if desc_length != None:
            self.effect_count = self.effect_count + 1
            self.desc_rt = self.desc_rt + desc_length

    def averageNameLength(self):
        return self.name_rt / self.card_count

    def averageDescLength(self):
        return self.desc_rt / self.effect_count

    def isReprintOnly(self):
        return self.card_count == 0

    def isNonEffectOnly(self):
        return self.effect_count == 0

    # initialise set data
    @staticmethod
    def initialise(cardsets, cards, noeffect):

        # remove sets with no tcg release
        cardsets = [set for set in cardsets if "tcg_date" in set]
        # convert to object array
        cardsets = [Set(set["set_name"], set["tcg_date"]) for set in cardsets]
        # sort by release date
        cardsets.sort(key=lambda set: set.tcg_date)

        # remove cards not released in a set and tokens
        cards = [card for card in cards if ("card_sets" in card and card["type"] != "Token")]

        for card in cards:

            # get index of first print set in cardsets
            index = Set.getFirstSet(cardsets, card["card_sets"])

            # ignore if no tcg release
            if index != None:

                # check if card has effect
                if card["name"] in noeffect:
                    cardsets[index].update(len(card["name"]))
                else:
                    cardsets[index].update(len(card["name"]), len(card["desc"]))

        # exclude reprint only sets
        return [set for set in cardsets if (not set.isReprintOnly())]

    # find the index of the first set each card is printed in
    @staticmethod
    def getFirstSet(cardsets, sets_printed):

        # list of set names for all sets card printed in
        print_names = [printset["set_name"] for printset in sets_printed]

        # search cardsets for a printed set
        for i, set in enumerate(cardsets):
            if set.name in print_names:
                # return index of first set found
                return i

        # return none if set not found (no tcg release)
        return None
