def choose_card(hand, valid_cards):
    if valid_cards:
        return max(valid_cards, key=lambda card: card.rank)
    return min(hand, key=lambda card: card.rank)