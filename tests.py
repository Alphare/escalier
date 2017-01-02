import models
from settings import COLORS, VALUES


class TestObjects:
    def test_game_state(self):
        game_state = models.GameState()
        assert game_state.number_of_cards == 1
        assert game_state.super_card == None
        assert game_state.trick_color == None
        assert game_state.played_cards == None
        assert game_state.tricks_per_player == None
        assert game_state.players == None
        assert game_state.deck == None


class TestGameRules:
    def test_deal_one_card(self):
        number_of_players = 4

        game_state = models.GameState()
        game_state.players = [models.BOT() for _ in range(0, number_of_players)]
        game_state.deal()
        assert game_state.number_of_cards == 1
        assert game_state.super_card.color in COLORS
        assert game_state.super_card.value in VALUES
        assert game_state.trick_color == None
        assert game_state.played_cards == None
        assert len(game_state.players) == number_of_players
        assert game_state.tricks_per_player == [0 for _ in game_state.players]
        for player in game_state.players:
            assert len(player.cards) == 1

        # Number of cards total is hardcoded if there's a mistake in the settings enum
        # The minus one is the super card
        assert len(game_state.deck.cards) == 52 - number_of_players - 1
