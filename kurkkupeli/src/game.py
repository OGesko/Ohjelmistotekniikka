from deck import Deck
from player import Player

def create_players():
    players = []
    num = int(input("how many players? (2-6) "))
    for _ in range(0, num):
        players.append(Player(input("player name: ")))
    print(f"players: {[x.name for x in players]}")
    return players

def deal_cards(deck, players):
    for _ in range(7):
        for player in players:
            player.hand.append(deck.deal())

def game_loop(players, deck):
    deck.shuffle()
    deal_cards(deck, players)
    first = 0
    while True:
        first = game_round(first, players)
        if all(len(player.hand) == 1 for player in players):
            break

    print("\n--- Final Cards ---")
    for player in players:
        print(f"{player.name}: {player.hand[0]}")

    # Determine loser
    loser = max(players, key=lambda p: p.hand[0])
    print(f"\nGame over! The loser is {loser.name} with {loser.hand[0]}")

def game_round(first, players):
    highest_card = None
    new_first = first
    for i in range(len(players)):
        player = players[(first + i) % len(players)]
        player.show_hand()
        print(f"card to beat: {highest_card}" if highest_card else "start round: ")

        valid = [card for card in player.hand if (highest_card is None) or (card >= highest_card)]
        smallest_card = min(player.hand)

        while True:
            choice = int(input("choose card by index"))
            card_to_play = player.hand[choice]
            if card_to_play in valid or (len(valid) == 0 and card_to_play == smallest_card):
                break
            print("invalid card")

        player.hand.remove(card_to_play)
        print(f"{player.name}: {card_to_play.display()}")

        if highest_card is None or card_to_play > highest_card:
            highest_card = card_to_play
            new_first = (first + i) % len(players)

    return new_first

def main():
    print("start game + help")
    deck = Deck()
    players = create_players()
    game_loop(players, deck)

main()
