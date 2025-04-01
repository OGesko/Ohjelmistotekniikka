import random
class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    def display(self):
        return (self.suite, self.rank)
class Deck:
    def __init__(self):
        self.deck = []
        suites = ["h","s","d","c"]
        for suite in suites:
            for rank in range(1,14):
                self.deck.append(Card(suite,rank))

    def suffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        else:
            return None

    def __iter__(self):
        return iter(self.deck)

pakka = Deck()
pakka.suffle()
for card in pakka:
    print(card.display())
