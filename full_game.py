"""
Реализация игры “Дурак”
"""

from deck_total import Card, Deck


MAX_CARDS = 10


class Hand:
    """Класс рука игрока"""

    def __init__(self, deck: Deck, name):
        self.cards = deck.draw(MAX_CARDS)
        self.name = name

    def __str__(self):
        return f'{self.name} [{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'

    def __repr__(self):
        return f'Карт в руке [{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'

    def __getitem__(self, item):
        return self.cards[item]

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.cards):
            return self.cards[self.index]
        raise StopIteration


class Game:
    """Класс игра"""

    def __init__(self, hand_1, hand_2):
        self.hand_1 = hand_1
        self.hand_2 = hand_2

    def attack(forward_player: Hand) -> Card:
        """Игрок атакует"""
        return forward_player.cards.pop(
            forward_player.cards.index(min(forward_player.cards))
        )

    def defend(forward_card: Card, player: Hand):
        """Другой игрок защищается.
        forward_card - карта атакующего
        player - рука отбивающегося"""
        res = [
            card
            for card in player
            if forward_card.equal_suit(card) and card > forward_card
        ]

        if res:
            return player.cards.pop(player.cards.index(min(res)))
        return None

    def add_card(table: list, forward_player: Hand):
        """Атакущюий игрок подкидыает карты с одинаковым значением"""
        cards_values = [card.value for card in table]
        res = [card for card in forward_player if card.value in cards_values]

        if res:
            return forward_player.cards.pop(forward_player.cards.index(min(res)))
        return None

    def take(player: Hand, deck: Deck) -> None:
        """Игрок берёт необходимое кол-во карт из колоды"""
        if len(player.cards) <= 10:
            number = MAX_CARDS - len(player.cards)
            max_num_of_cards = min(len(deck.cards), number)
            player.cards += deck.draw(max_num_of_cards)

    def game(hand_1: Hand, hand_2: Hand) -> bool:
        """Реализация игры. Первый ход за первой рукой.
        Если защищающийся игрок не отбивается, то атакующий подкидывает все оставшиеся карты
        с одинаковым значением, защищающийся забирает все карты, рука не меняется.
        Если защищающийся игрок отбился, то атакующий подбрасывает ему карты
        с одинаковым значением, если имеет такие, если таких нет,
        то у нас Бито, атакующий и защищающийся игроки меняются местами."""

        table = []  # Игровой стол
        change = False  # Флаг смены руки

        attack_card = Game.attack(hand_1)
        print(f"Ходит {hand_1.name} {attack_card}")
        table += [attack_card]
        has_card = True  # Флаг наличия карт, которыми можно атаковать в одном ходу
        defend_card = Game.defend(attack_card, hand_2)

        if defend_card:
            print(f"Отбивается {hand_2.name} {defend_card}")
            table.append(defend_card)
        else:
            add_card = Game.add_card(table, hand_1)
            while add_card:
                print(f"{hand_1.name} подкидывает карту {add_card}")
                table.append(add_card)
                add_card = Game.add_card(table, hand_1)
            print(f"{hand_2.name} забирает все карты со стола")
            hand_2.cards += table
            table.clear()
            return change

        while has_card:
            add_card = Game.add_card(table, hand_1)
            if add_card and hand_2.cards:
                table.append(add_card)
                print(f"{hand_1.name} подкидывает карту {add_card}")
                defend_card = Game.defend(add_card, hand_2)
                if defend_card:
                    table.append(defend_card)
                    print(f"{hand_2.name} отбивается {defend_card}")
                else:
                    print(f"{hand_2.name} не может отбиться")
                    add_card = Game.add_card(table, hand_1)
                    while add_card:
                        table.append(add_card)
                        print(f"{hand_1.name} подкидывает карту {add_card}")
                        add_card = Game.add_card(table, hand_1)
                    print(f"{hand_2.name} забирает все карты со стола")
                    hand_2.cards += table
                    table.clear()
                    has_card = False
                    return change
            else:
                print("Бито")
                table.clear()
                change = True
                has_card = False
                return change


game_deck = Deck()
game_deck.shuffle()

game_hand_1 = Hand(game_deck, "Asia")
game_hand_2 = Hand(game_deck, "Vania")
print(game_hand_1)
print(game_hand_2)
print(game_deck)

card_game = Game(game_hand_1, game_hand_2)

while (
    game_hand_1.cards and game_hand_2.cards
):  # Пока в обеих рукахесть карты, то игра продолжается
    GAME = Game.game(game_hand_1, game_hand_2)
    print(game_hand_1)
    print(game_hand_2)
    Game.take(game_hand_1, game_deck)
    Game.take(game_hand_2, game_deck)
    print(game_hand_1)
    print(game_hand_2)
    if GAME:
        game_hand_1, game_hand_2 = game_hand_2, game_hand_1

if game_hand_1:
    print(f"Победил игрок {game_hand_1.name}")
else:
    print(f"Победил игрок {game_hand_2.name}")
