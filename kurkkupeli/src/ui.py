import pygame
import os
from game import Game, get_valid_cards
from bot import choose_card

pygame.init()

# Settings
WIDTH, HEIGHT = 1000, 600
CARD_WIDTH, CARD_HEIGHT = 80, 120
HAND_Y = 450
CENTER_Y = 200
BG_COLOR = (0, 120, 0)
font = pygame.font.SysFont(None, 36)
button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)

# delays
bot_delay = 500
round_delay = 2500
pause_before_next_round = False
pause_timer = 0

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kurkku Card Game")
clock = pygame.time.Clock()
running = True
game_over = False

def show_start_screen():
    selecting = True
    while selecting:
        screen.fill((30, 30, 30))
        title = font.render("Choose number of bot opponents (1–5)", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        buttons = []
        for i in range(1, 6):
            btn_rect = pygame.Rect(100 + i * 120, 200, 100, 50)
            pygame.draw.rect(screen, (200, 200, 200), btn_rect)
            btn_text = font.render(str(i), True, (0, 0, 0))
            screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
            buttons.append((btn_rect, i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn_rect, count in buttons:
                    if btn_rect.collidepoint(event.pos):
                        return count

        pygame.display.flip()
        clock.tick(60)

PILE_POSITIONS = {}

def set_bot_positions(players):
    spacing = WIDTH // (len(players) + 1)
    for i, player in enumerate(players):
        x = spacing * (i + 1) - CARD_WIDTH // 2
        y = 50  # top of screen
        PILE_POSITIONS[player.name] = (x, y)

bot_count = show_start_screen()
game = Game(bot_count)
set_bot_positions(game.players)
game.start_round()

# Helper to load images
def load_card_image(card):
    filename = f"{card.rank}{card.suite}.png"
    path = os.path.join("src", "images", filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
    except FileNotFoundError:
        print(f"Missing image: {filename}")
        return pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

# Main loop variables
played_cards = []

def draw_hand(player_hand, valid_cards):
    card_sprites = []
    for i, card in enumerate(player_hand):
        image = load_card_image(card)
        rect = image.get_rect(topleft=(100 + i * (CARD_WIDTH + 10), HAND_Y))
        if card not in valid_cards:
            image.set_alpha(100)
        card_sprites.append((card, image, rect))
    return card_sprites

def draw_played_cards():
    # At the end, show the final card(s) in each player's hand
    if game_over:
        for player in game.players:
            for card in player.hand:
                if player.name in PILE_POSITIONS:
                    x, y = PILE_POSITIONS[player.name]
                    image = load_card_image(card)
                    screen.blit(image, (x, y + 20))
    else:
        # During the game, show last played cards as before
        latest = {}
        for card, player_name in played_cards:
            latest[player_name] = card

        for player_name, card in latest.items():
            if player_name in PILE_POSITIONS:
                x, y = PILE_POSITIONS[player_name]
                image = load_card_image(card)
                screen.blit(image, (x, y + 20))
                name_text = font.render(player_name, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(x + CARD_WIDTH // 2, y))
                screen.blit(name_text, name_rect)

def draw_remaining_cards():
    y_offset = 300
    for player in game.players:
        cards_text = f"{player.name}'s remaining cards: " + ", ".join([f"{card.rank}{card.suite}" for card in player.hand])
        text = font.render(cards_text, True, (255, 255, 255))
        screen.blit(text, (50, y_offset))
        y_offset += 30

while running:
    screen.fill(BG_COLOR)

    if not game_over:
        player_hand = game.players[0].hand
        current_player = game.get_current_player()
        valid_cards = get_valid_cards(current_player.hand, game.highest_card)
        hand_sprites = draw_hand(player_hand, valid_cards)

        draw_played_cards()
        draw_remaining_cards()

        if not game.is_turn_done():
            if "Bot" in current_player.name:
                pygame.display.flip()
                pygame.time.delay(bot_delay)
                selected_card = choose_card(current_player.hand, valid_cards)
                game.play_turn(selected_card)
                played_cards.append((selected_card, current_player.name))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, (card, image, rect) in enumerate(hand_sprites):
                        if rect.collidepoint(pos) and card in valid_cards:
                            print(f"{current_player.name} played: {card}")
                            game.play_turn(card)
                            played_cards.append((card, current_player.name))
                            break
        else:
            print("Turn is done. Waiting for the next round.")

        if game.is_turn_done() and not pause_before_next_round:
            # Transition to the next round
            pause_before_next_round = True
            pause_timer = pygame.time.get_ticks()

        if pause_before_next_round:
            if pygame.time.get_ticks() - pause_timer >= round_delay:
                game.end_round()
                game.start_round()
                played_cards.clear()
                pause_before_next_round = False

        # End game
        if game.is_game_over():
            loser, last_card_played = game.get_loser(played_cards)
            print(f"Game over! Loser is {loser.name} with {last_card_played}")
            game_over = True

        for card, image, rect in hand_sprites:
            screen.blit(image, rect.topleft)

    elif game_over:
        draw_played_cards()

        # **Display the loser**
        loser, last_card_played = game.get_loser(played_cards)

        for player_name, (x, y) in PILE_POSITIONS.items():
            if player_name == loser.name:
                # Draw "Loser" below the losing player's pile
                loser_text = font.render("Loser", True, (255, 0, 0))
                loser_rect = loser_text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT + 50))
                screen.blit(loser_text, loser_rect)

        # Display remaining cards
        draw_remaining_cards()

        # Announce the loser
        if last_card_played:
            loser_announcement = f"{loser.name} loses with {last_card_played.rank}{last_card_played.suite}!"
        else:
            loser_announcement = f"{loser.name} loses!"
        loser_text = font.render(loser_announcement, True, (255, 255, 255))
        screen.blit(loser_text, (WIDTH // 2 - loser_text.get_width() // 2, HEIGHT // 2 - 50))

        # Draw the "New Round" button
        pygame.draw.rect(screen, (200, 200, 200), button_rect)
        text = font.render("New Round", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(pos):
                    # Restart the game
                    game = Game(bot_count)
                    game.start_round()
                    played_cards.clear()
                    game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
