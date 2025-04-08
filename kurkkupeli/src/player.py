from deck import Card
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []

    def show_hand(self):
        for id_x, card in enumerate(self.hand):
            print(f"{id_x}: {card.display()}")

    def play_card(self):
        pass

    def change_hand(self):
        pass

    def __str__(self):
        return f"{self.name} {self.hand}"
