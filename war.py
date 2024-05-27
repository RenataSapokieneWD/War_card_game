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
        return self.rank_values[self.rank] < self.rank_values[other.rank]
    def __gt__(self, other):
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
            rank = input("Enter the rank of the card: 2-10, J, Q, K, A : ",).strip().upper()
            suit = input("Enter the suit: Hearts, Diamonds, Clubs, Spades: ",).strip().capitalize()
            if rank in Card.ranks and suit in Card.suits:
                player_card = Card(rank,suit)
                if player_card in self.player1.hand:
                    self.player1.hand.remove(player_card)
                    return player_card
                else:
                    print("You do not have this card in your hand. Try again.")
            else:
                print("Invalid rank or suit. Try again.")

    def play_round(self):
            player_card = self.get_player_card()
            computer_card = Deck().deal()
            round_cards = []
            round_cards.append([player_card, computer_card])
            if player_card > computer_card:
                Player("Player 1").collect_cards(round_cards) #need stack where to keep won cards
            elif player_card < computer_card:
                Player("Computer").collect_cards(round_cards)  #need stack where to keep won cards
            else:
                self.handle_war()
        
        

    def handle_war(self, p1_cards, p2_cards):
        pass

    def determine_winner(self):
        pass

    def play_game(self):
        self.play_round()


if __name__ == "__main__":
    game = WarGame("Player 1", "Computer")
    game.play_game()
