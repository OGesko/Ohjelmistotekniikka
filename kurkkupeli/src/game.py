from deck import Deck
from player import Player

def create_players(bots):
    players = [Player("You")]
    for i in range(bots):
        players.append(Player(f"Bot_{i+1}"))
    #print(f"players: {[x.name for x in players]}")
    return players

def deal_cards(deck, players, cards_per_player=7):
    for _ in range(cards_per_player):
        for player in players:
            player.hand.append(deck.deal())

def get_valid_cards(hand, highest_card):
    if highest_card is None:
        return hand
    valid = [card for card in hand if card >= highest_card]
    return valid if valid else [min(hand)]

def play_card(player, card):
    player.hand.remove(card)
    return card

def game_over(players):
    return all(len(player.hand) == 1 for player in players)

def get_final_loser(players, played_cards):
    loser = max(players, key=lambda p: max(card.rank for card in p.hand))
    # Find the last card played by the loser
    last_card_played = next((card for card, player_name in played_cards if player_name == loser.name), None)
    return loser, last_card_played

class Game:
    def __init__(self, bot_count):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = create_players(bot_count)
        deal_cards(self.deck, self.players)
        self.first_player_index = 0
        self.highest_card = None
        self.new_first_player_index = 0
        self.current_turn = 0
        self.round_done = False

    def start_round(self):
        self.highest_card = None
        self.new_first_player_index = self.first_player_index
        self.current_turn = 0
        self.round_done = False

    def get_current_player(self):
        index = (self.first_player_index + self.current_turn) % len(self.players)
        return self.players[index]

    def is_turn_done(self):
        # Check if the current turn has reached the total number of players
        return self.current_turn >= len(self.players)

    def play_turn(self, card):
        if self.is_turn_done():
            print("Turn is already done. No more moves allowed.")
            return

        player = self.get_current_player()
        play_card(player, card)

        if self.highest_card is None or card.rank >= self.highest_card.rank:
            self.highest_card = card
            self.new_first_player_index = (self.first_player_index + self.current_turn) % len(self.players)

        self.current_turn += 1
        print(f"Played {card} by {player.name}, Current Turn: {self.current_turn}")

    def end_round(self):
        self.first_player_index = self.new_first_player_index
        self.round_done = True

    def is_game_over(self):
        return game_over(self.players)

    def get_loser(self, played_cards):
        # Determine the player with the highest card in their hand
        loser = max(self.players, key=lambda p: max((card.rank for card in p.hand), default=0))
        last_card_played = max(loser.hand, key=lambda c: c.rank, default=None)
        return loser, last_card_played
