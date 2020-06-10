import requests, time, threading, sys, itertools


class Deck:
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """
    
    def __init__(self):
        """Initializes the Deck with 52 cards. """

        self.base_url = 'https://deckofcardsapi.com/api/deck/'
        new_deck_url = self.base_url + 'new/shuffle/'
        param = {'deck_count': 1}
        new_deck = requests.get(new_deck_url, params=param).json()
        self.deck_id = new_deck.get('deck_id', -1)
        print('deck created', self.deck_id)

    def pop_card(self):
        """Removes and returns a card from the deck. """
        remove_card_url = self.base_url + self.deck_id + '/draw/'
        removed_card_json = requests.get(remove_card_url).json()
        self.popped_card = removed_card_json['cards'][0]['code']
        return self.popped_card

    def shuffle(self):
        """Shuffles the cards in this deck."""

        shuffle_url = self.base_url + self.deck_id + '/shuffle/'
        res = requests.get(shuffle_url).json()
        print('deck shuffled')

    def move_cards(self, hand, num=1):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        cards = []
        for i in range(num):
            cards.append(self.pop_card())
        str_cards = ",".join(cards)
        param = {"cards": str_cards}
        move_url = self.base_url + self.deck_id + '/pile/' + hand + '/add/'
        res = requests.get(move_url, params=param).json()
        if res['success']:
            return True
            #print(f'cards moved to {hand}')
        else:
            print("error in moving cards")
        return

    def distribute_cards(self, num, player_list):
        """ Distributes cards to players """

        done = False
        # here is the animation
        def animated_loading():
            for char in itertools.cycle('/-\\|'):
                if done:
                    break
                sys.stdout.write('\r' + 'Distributing Cards... ' + char)
                time.sleep(.2)
                sys.stdout.flush()

        t = threading.Thread(target=animated_loading)
        t.start()

        # long process here
        for i in range(num):
            for player in player_list:
                self.move_cards(player)
        done = True


class Hand(Deck):
    """Represents a hand of playing cards."""

    def __init__(self):

        self.hand = []

    def player_hand(self, hand, display=False):
        """ Displays player's cards """

        self.hand = []
        hand_url = self.base_url + self.deck_id + '/pile/' + hand + '/list/'
        res = requests.get(hand_url).json()
        t = res['piles'][hand]['cards']
        for card in range(len(t)):
            self.hand.append(t[card]['code'])
        if display:
            print(f'{hand} cards -> {self.hand}')
        if hand == 'dealer':
            self.dealer_hand = self.hand
        return self.hand

    def finalPlayerHand(self, deck_obj, hand):
        """ adds player's hand with dealer's open 5 cards
            hand = player name
        """

        player_hand = self.player_hand(hand=hand)
        dealer_hand = self.player_hand(hand='dealer')
        final_player_hand = player_hand + dealer_hand
        return final_player_hand

    def finalPlayerHandList(self, player_list):
        """ adds player's hand with dealer's open 5 cards
            param = player name list
            return = players name dictionary
        """
        player_dict = {}
        dealer_hand = self.player_hand(hand='dealer')
        for name in player_list:
            player_hand = self.player_hand(hand=name)
            final_player_hand = player_hand + dealer_hand
            player_dict[name] = final_player_hand
        player_dict['dealer'] = dealer_hand
        return player_dict

    def highCardAllPlayers(self, player_list):
        '''
        :param player_list:
        :return: dict ('playerName': highCard)
        '''
        highCards = {}
        for name in player_list:
            p_Cards = self.player_hand(name)
            highCards[name] = self.highCard(p_Cards)
        return highCards

    def dealerHighCard(self):
        d_cards = self.player_hand('dealer')
        dealer_high_c = self.highCard(d_cards)
        return dealer_high_c