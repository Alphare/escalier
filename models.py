import random

import attr

from settings import COLORS, VALUES


def get_cards_of_colors(cards, colors):
    return [card for card in cards if card.color in colors]


@attr.s
class PlayerProfile:
    name = attr.ib(default="Player")

    def change_name(self, new_name):
        self.name = str(new_name)


@attr.s
class Player:
    profile = attr.ib(default=PlayerProfile())
    score = attr.ib(default=0)
    cards = attr.ib(default=None)
    bet = attr.ib(default=0)

    def _select_bet_number(self, maximum):
        pass

    def place_bet(self, game_state):
        self._select_bet_number(game_state.number_of_cards)

    def _choose_card(self, available_cards):
        pass

    def choose_card(self, trick_color, super_card_color):
        if trick_color is not None:
            trick_color_cards = get_cards_of_colors(self.cards, [trick_color])
            if trick_color_cards == []:
                super_card_color_cards = get_cards_of_colors(self.cards, [super_card_color])
                if super_card_color_cards == []:
                    self._choose_card(self.cards)
                else:
                    self._choose_card(super_card_color_cards)
            else:
                self._choose_card(trick_color_cards)
        else:
            self._choose_card(self.cards)


@attr.s
class GameState:  # TODO split into GameState/RoundState/TrickState
    number_of_cards = attr.ib()
    super_card = attr.ib()
    trick_color = attr.ib()
    played_cards = attr.ib()
    tricks_per_player = attr.ib()
    players = attr.ib()
    deck = attr.ib()

    def compute_scores(self):
        for index, player in enumerate(self.players):
            player_tricks_count = self.tricks_per_player[index]
            player.score += sum(player_tricks_count)
            if player.bet == player_tricks_count:
                player.score += 10

    def _get_best_card(self, card, current_best_card):
        """
        Assumes cards are of the same color
        """
        if VALUES.index(card) > VALUES.index(current_best_card):
            return card
        else:
            return current_best_card

    def get_trick_winner(self):
        super_card_color = self.super_card.color
        possible_winning_cards = get_cards_of_colors(self.played_cards,
                                                     (super_card_color, self.trick_color))
        current_best_card = possible_winning_cards.pop(0)  # Minor optimization
        for card in possible_winning_cards:
            if card.color == super_card_color:
                if current_best_card.color == super_card_color:
                    current_best_card = self._get_best_card(card, current_best_card)
                else:
                    current_best_card = card

            else:
                if card.color == self.trick_color:
                    if current_best_card.color == self.trick_color:
                        current_best_card = self._get_best_card(card, current_best_card)
                    else:
                        current_best_card = card
                else:
                    if not current_best_card.color == self.trick_color:
                        current_best_card = self._get_best_card(card, current_best_card)

        return current_best_card.player

    def deal(self):
        self.deck = Deck()
        self.played_cards = []
        self.tricks_per_player = [0 for _ in self.players]
        for player in self.players:
            player.cards = []
            for card_count in range(0, self.number_of_cards):
                picked_card = self.deck.pick()
                picked_card.player = player
                player.cards.append(picked_card)

            self.super_card = self.deck.pick()

    def play_trick(self):
        for index, player in enumerate(self.players):
            chosen_card = player.choose_card(self.trick_color, self.super_card.color)

            if self.trick_color is None:
                self.trick_color = chosen_card.color

            self.played_cards.append(chosen_card)

            if index == len(self.players) - 1:  # Last iteration
                trick_winner_index = self.players.index(self.get_trick_winner)
                self.tricks_per_player[trick_winner_index] += 1

    def place_bets(self):
        for player in self.players:
            player.place_bet()


@attr.s
class Card:
    color = attr.ib()
    value = attr.ib()
    player = attr.ib()

    @property
    def verbose_name(self):
        return "{} of {}".format(self.color, self.value)


class Deck:
    def __init__(self):
        self.cards = []
        for color in COLORS:
            for value in VALUES:
                self.cards.append(Card(color=color, value=value))

        self._shuffle()

    def _shuffle(self):
        random.shuffle(self.cards)

    def pick(self):
        return self.cards.pop(random.choice(0, len(self.cards)))
