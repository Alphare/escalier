import random

import attr

from settings import COLORS, VALUES


def get_cards_of_colors(cards, colors):
    return [card for card in cards if card.color in colors]


@attr.s
class GameState:  # TODO split into GameState/RoundState/TrickState
    number_of_cards = attr.ib(default=1)
    super_card = attr.ib(default=None)
    trick_color = attr.ib(default=None)
    played_cards = attr.ib(default=None)
    tricks_per_player = attr.ib(default=None)
    players = attr.ib(default=None)
    deck = attr.ib(default=None)

    def compute_scores(self):
        for index, player in enumerate(self.players):
            player_tricks_count = self.tricks_per_player[index]
            player.score += player_tricks_count
            if player.bet == player_tricks_count:
                player.score += 10

        print("**********")
        print("SCOREBOARD")
        print("**********")
        for player in self.players:
            print("{}: {}".format(player, player.score))
        print("**********")

    def _get_best_card(self, card, other_card):
        """
        Assumes cards are of the same color
        """
        if VALUES.index(card.value) > VALUES.index(other_card.value):
            return card
        else:
            return other_card

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

        trick_winner = current_best_card.player
        print("=================")
        print('{} wins the trick with a {}'.format(trick_winner, current_best_card))
        return trick_winner

    def deal(self):
        self.deck = Deck()
        self.tricks_per_player = [0 for _ in self.players]
        self.super_card = self.deck.pick()
        print("Super card is a {}".format(self.super_card))
        for player in self.players:
            player.cards = []
            for card_count in range(0, self.number_of_cards):
                picked_card = self.deck.pick()
                picked_card.player = player
                player.cards.append(picked_card)

    def play_trick(self):
        self.trick_color = None
        self.played_cards = []
        for index, player in enumerate(self.players):
            chosen_card = player.choose_card(self.trick_color, self.super_card.color)

            if self.trick_color is None:
                self.trick_color = chosen_card.color

            self.add_card_to_played_cards(player, chosen_card)

        trick_winner_index = self.players.index(self.get_trick_winner())
        self.tricks_per_player[trick_winner_index] += 1

    def place_bets(self):
        for player in self.players:
            player.place_bet(self.number_of_cards)

    def add_card_to_played_cards(self, player, card):
        print("{} played a {}".format(player, card))
        self.played_cards.append(card)


@attr.s
class PlayerProfile:
    name = attr.ib(default="Player")

    def change_name(self, new_name):
        self.name = str(new_name)


@attr.s
class Player:
    profile = attr.ib(default=attr.Factory(PlayerProfile))
    score = attr.ib(default=0)
    cards = attr.ib(default=None)
    bet = attr.ib(default=0)
    human = attr.ib(default=False)

    def _select_bet_number(self, max_number):
        number = -1
        while number < 0 or number > max_number:
            number = int(input('Please enter your bet:\n'))
        return number

    def place_bet(self, max_number):
        print("You've been dealt {} cards\n=====================".format(max_number))
        print(", ".join([str(card) for card in self.cards]))
        self.bet = self._select_bet_number(max_number)

    def _choose_card(self, available_cards):
        number = -1
        while number < 0 or number > len(available_cards):
            print('Available cards\n===============')
            print(", ".join([str(card) for card in available_cards]))
            number = int(input('Please choose your card:\n'))
        chosen_card = available_cards[number]
        self.cards.remove(chosen_card)
        return chosen_card

    def choose_card(self, trick_color, super_card_color):
        if trick_color is not None:
            trick_color_cards = get_cards_of_colors(self.cards, [trick_color])
            if trick_color_cards == []:
                super_card_color_cards = get_cards_of_colors(self.cards, [super_card_color])
                if super_card_color_cards != []:
                    return self._choose_card(super_card_color_cards)
            else:
                return self._choose_card(trick_color_cards)

        return self._choose_card(self.cards)

    def __str__(self):
        return self.profile.name


class BOT(Player):
    def place_bet(self, max_number):
        self.bet = random.randint(0, max_number)
        print("{} bet {}".format(self, self.bet))

    def _choose_card(self, available_cards):
        return random.choice(available_cards)

    def __str__(self):
        return "BOT {}".format(self.profile.name)

@attr.s
class Card:
    color = attr.ib()
    value = attr.ib()
    player = attr.ib(default=None)

    def __str__(self):
        return "{} of {}".format(self.value, self.color)


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
        return self.cards.pop()
