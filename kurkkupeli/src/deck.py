import random
class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    def display(self):
        return f"{self.suite}, {self.rank}"

    def __str__(self):
        return self.display()

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

class Deck:
    def __init__(self):
        self.deck = []
        suites = ["h","s","d","c"]
        for suite in suites:
            for rank in range(2,15):
                self.deck.append(Card(suite,rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return None

    def __iter__(self):
        return iter(self.deck)
