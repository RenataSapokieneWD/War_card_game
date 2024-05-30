import random

class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    rank_values = {rank: value for value, rank in enumerate(ranks, 2)}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        if self.rank_values[self.rank] == self.rank_values[other.rank]:
            return self.suits.index(self.suit) < self.suits.index(other.suit)
        return self.rank_values[self.rank] < self.rank_values[other.rank]

    def __gt__(self, other):
        if self.rank_values[self.rank] == self.rank_values[other.rank]:
            return self.suits.index(self.suit) > self.suits.index(other.suit)
        return self.rank_values[self.rank] > self.rank_values[other.rank]

    def __eq__(self, other):
        return self.rank_values[self.rank] == self.rank_values[other.rank]


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self):
        if self.hand:
            return self.hand.pop(0)
        else:
            return None

    def collect_cards(self, cards):
        self.hand.extend(cards)

    def has_cards(self):
        return len(self.hand) > 0

    def sort_hand(self):
        self.hand.sort()

    def print_hand(self):
        self.sort_hand()
        for card in self.hand:
            print(card)

    def __repr__(self):
        return f"{self.name} with {len(self.hand)} cards"


class WarGame:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.deck = Deck()
        self.deal_cards()

    def deal_cards(self):
        while self.deck.cards:
            self.player1.collect_cards([self.deck.deal()])
            self.player2.collect_cards([self.deck.deal()])

    def get_player_card(self):
        while True:
            print("Your hand:")
            self.player1.print_hand()
            rank = input("Enter the rank of your card (2-10, J, Q, K, A): ").strip().upper()
            suit = input("Enter the suit of your card (Hearts, Diamonds, Clubs, Spades): ").strip().capitalize()
            if rank in Card.ranks and suit in Card.suits:
                player_card = Card(rank, suit)
                if player_card in self.player1.hand:
                    self.player1.hand.remove(player_card)
                    return player_card
                else:
                    print("You do not have this card in your hand. Try again.")
            else:
                print("Invalid rank or suit. Try again.")

    def play_round(self):
        if not self.player1.has_cards() or not self.player2.has_cards():
            return False  # Game over
        p1_card = self.get_player_card()
        p2_card = self.player2.draw_card()
        print(f"{self.player1.name} plays {p1_card}")
        print(f"{self.player2.name} plays {p2_card}")
        if p1_card > p2_card:
            self.player1.collect_cards([p1_card, p2_card])
            print(f"{self.player1.name} wins the round!")
        elif p2_card > p1_card:
            self.player2.collect_cards([p1_card, p2_card])
            print(f"{self.player2.name} wins the round!")
        else:
            print("War!")
            self.handle_war([p1_card], [p2_card])
        return True

    def handle_war(self, p1_cards, p2_cards):
        if len(self.player1.hand) < 4 or len(self.player2.hand) < 4:
            print("Not enough cards for war! Ending game.")
            return
        p1_cards.extend(self.player1.draw_card() for _ in range(4))
        p2_cards.extend(self.player2.draw_card() for _ in range(4))
        print(f"{self.player1.name} plays {p1_cards[-1]} in war")
        print(f"{self.player2.name} plays {p2_cards[-1]} in war")
        if p1_cards[-1] > p2_cards[-1]:
            self.player1.collect_cards(p1_cards + p2_cards)
            print(f"{self.player1.name} wins the war!")
        elif p2_cards[-1] > p1_cards[-1]:
            self.player2.collect_cards(p1_cards + p2_cards)
            print(f"{self.player2.name} wins the war!")
        else:
            print("Another War!")
            self.handle_war(p1_cards, p2_cards)

    def determine_winner(self):
        if len(self.player1.hand) > len(self.player2.hand):
            return self.player1.name
        elif len(self.player2.hand) > len(self.player1.hand):
            return self.player2.name
        else:
            return "No one, it's a tie!"

    def play_game(self):
        round_number = 1
        while self.play_round():
            print(f"End of round {round_number}")
            round_number += 1
            print(f"{self.player1}")
            print(f"{self.player2}")
            print("-" * 20)
            if input("Press Enter to continue to the next round or type 'exit' to stop: ").strip().lower() == 'exit':
                break
        winner = self.determine_winner()
        print(f"The winner is {winner}!")


if __name__ == "__main__":
    game = WarGame("Player 1", "Computer")
    game.play_game()


