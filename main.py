import random

from models import GameState, Player, BOT
from settings import PLAYER_NAMES


def game_loop():
    game_on = True
    game_state = GameState()
    human = Player()
    human.profile.name = "Human"
    game_state.players = [human]
    game_state.players.extend([BOT() for _ in range(0, 3)])

    while (game_on and game_state.number_of_cards < 11):  # Rounds
        game_state.deal()
        game_state.place_bets()

        for _ in range(0, game_state.number_of_cards):
            game_state.play_trick()

        game_state.compute_scores()

        game_state.number_of_cards += 1


if __name__ == '__main__':

    game_loop()
