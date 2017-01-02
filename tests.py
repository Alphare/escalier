import models
from settings import COLORS, VALUES


class TestObjects:
    def test_game_state(self):
        game_state = models.GameState()
        assert game_state.number_of_cards == 1
        assert game_state.super_card == None
        assert game_state.trick_color == None
        assert game_state.played_cards == []
        assert game_state.tricks_per_player == []
        assert game_state.players == []
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
        assert game_state.played_cards == []
        assert len(game_state.players) == number_of_players
        assert game_state.tricks_per_player == [0 for _ in game_state.players]
        for player in game_state.players:
            assert len(player.cards) == 1

        # Number of cards total is hardcoded if there's a mistake in the settings enum
        # The minus one is the super card
        assert len(game_state.deck.cards) == 52 - number_of_players - 1

    def test_get_trick_winner(self):
        number_of_players = 4

        game_state = models.GameState()
        game_state.players = [models.BOT() for _ in range(0, number_of_players)]

        game_state.deck = models.Deck()
        cards_to_pick = [('2', 'Hearts'), ('Ace', 'Spades'), ('King', 'Spades'), ('9', 'Diamonds')]
        game_state.super_card = game_state.deck.pick_card(value='6', color='Hearts')
        game_state.trick_color = 'Spades'

        for player, card_tuple in zip(game_state.players, cards_to_pick):
            card = game_state.deck.pick_card(*card_tuple)
            card.player = player
            game_state.played_cards.append(card)

        assert game_state.get_trick_winner() is game_state.players[0]