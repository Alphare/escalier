from models import GameState, Player

def game_loop():
    game_on = True
    game_state = GameState()
    game_state.players = [Player() for _ in range(0, 1)]

    while (game_on and game_state.number_of_cards < 11):  # Rounds
        game_state.deal()
        game_state.place_bets()

        for _ in range(0, game_state.number_of_cards):
            game_state.play_trick()

        game_state.compute_scores()

        game_state.number_of_cards += 1


if __name__ == '__main__':

    game_loop()