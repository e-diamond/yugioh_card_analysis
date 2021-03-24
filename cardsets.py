
class Set:

    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.card_count = 0
        self.character_rt = 0

    def update(self, length):
        self.card_count = self.card_count + 1
        self.character_rt = self.character_rt + length

    def getAverageLength(self):
        return self.character_rt / self.card_count

    def isReprintOnly(self):
        if self.card_count == 0:
            return True
        else:
            return False
