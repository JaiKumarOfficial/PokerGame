import requests
from Card import Deck, Hand



class Ranks:

    def histogram(self, card_list):
        """ RETURNS sorted dict {suit: count(suit)}"""

        hist = {}
        temp_suits = []
        for i in card_list:
            temp_suits.append(i[1])
        for card in card_list:
            hist[card[1]] = temp_suits.count(card[1])
        sorted_hist = sorted(hist.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return dict(sorted_hist)

    def isRoyalFlush(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        hist = self.histogram(final_player_hand)
        for count in hist.values():
            if count >= 5:
                key = list(hist.keys())[0]
                royal_flush = ['A'+ key, 'K'+ key, 'Q'+ key,'J'+ key, '0'+ key]
                if set(royal_flush).issubset(set(final_player_hand)):
                    return True
        return False

    def isStraightFlush(self, Hand_obj, deck_obj, hand):

        flush = self.isFlush(Hand_obj, deck_obj, hand)
        if flush:
            final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
            hist = self.histogram(final_player_hand)
            for count in hist.values():
                if count >= 5:
                    key = list(hist.keys())[0]
            straight = self.isStraight(Hand_obj, deck_obj, hand, suits=[key])
            if straight:
                return True
            else:
                return False
        else:
            return False

    def isFlush(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        hist = self.histogram(final_player_hand)
        for count in hist.values():
            if count >= 5:
                return True
        return False

    def isStraight(self, Hand_obj, deck_obj, hand, suits=None):

        suits = suits
        num   = ['A','2','3','4','5','6','7','8','9','0','J','Q','K','A']
        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        if suits != None:
            for s in suits:
                count = 0
                for i in num:
                    card = i+s
                    if card in final_player_hand:
                        count += 1
                        if count == 5:
                            return True
                    else:
                        count = 0
        else:
            only_num = [num[0] for num in final_player_hand]
            count = 0
            for i in num:
                if i in only_num:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def isFourOfKind(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        num = [i[0] for i in final_player_hand]
        for i in num:
            if num.count(i) >= 4:
                return True
        return False

    def isFullHouse(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        num = [i[0] for i in final_player_hand]
        for i in num:
            if num.count(i) >= 3:
                temp = [j for j in num if j != i]
                for elem in temp:
                    if temp.count(elem) >= 2:
                        return True
        return False

    def isThreeOfKind(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        num = [i[0] for i in final_player_hand]
        for i in num:
            if num.count(i) >= 3:
                return True
        return False

    def isTwoOfKind(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        num = [i[0] for i in final_player_hand]
        for i in num:
            if num.count(i) >= 2:
                temp = [j for j in num if j != i]
                for elem in temp:
                    if temp.count(elem) >= 2:
                        return True
        return False

    def isPair(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        num = [i[0] for i in final_player_hand]
        for i in num:
            if num.count(i) >= 2:
                return True
        return False

    def highCard(self, Hand_obj, deck_obj, hand):

        final_player_hand = Hand.finalPlayerHand(Hand_obj, deck_obj, hand)
        sort_order = ['A','K','Q','J','0','9','8','7','6','5','4','3','2']
        res = [i for x in sort_order for i in final_player_hand if i[0] == x]
        return res[0]

    def compare(self, player_names, hand, deck):

        game = {}
        for name in player_names:
            rank_res = {}

            rank_res.update(RoyalFlush = poker.isRoyalFlush(hand, deck, name))
            rank_res.update(StraightFlush = poker.isStraightFlush(hand, deck, name))
            rank_res.update(FourOfKind = poker.isFourOfKind(hand, deck, name))
            rank_res.update(FullHouse= poker.isFullHouse(hand, deck, name))
            rank_res.update(Flush = poker.isFlush(hand, deck, name))
            rank_res.update(Straight = poker.isStraight(hand, deck, name))
            rank_res.update(ThreeOfKind= poker.isThreeOfKind(hand, deck, name))
            rank_res.update(TwoOfKind = poker.isTwoOfKind(hand, deck, name))
            rank_res.update(Pair = poker.isPair(hand, deck, name))
            rank_res.update(highCard = poker.highCard(hand, deck, name))
            game[name] = rank_res
        lst = []
        for name in player_names:
            index = 1
            for key, val in game[name].items():
                if val:
                    lst.append((key, name, index))
                    break
                else:
                    index += 1
        if len(lst) != 0:
            # player got any rank !!
            sort_lst = sorted(lst, key=lambda kv:(kv[2]))
            isDraw, winner = self.winner(sort_lst)
            if isDraw:
                drawNames = ""
                for enum, val in list(enumerate(winner, 1)):
                    if enum != len(list(enumerate(winner))):
                        drawNames += f"{val[1]}, "
                    else:
                        drawNames += val[1]
                return "Game draw b/w " + drawNames + " with " + str(winner[0][0])
            return f"{winner[1]} won with {winner[0]}"
        else:
            # check winner acc to high card
            highCard_list = []
            for name in player_names:
                print(game[name].get('highCard'), -1)
                highCard_list.append((name, game[name]['highcard']))
            isDraw, res = self.draw(highCard_list)
            return f"{res[0]} won with {res[1]} high card"

    def draw(self, list):
        isDraw = False
        num_rank= ['A','K','Q','J','0','9','8','7','6','5','4','3','2']
        suit_rank = ['S','H','D','C']
        sortNumRank = [i for x in num_rank for i in list if i[1][0] == x]
        count = 1
        t = [sortNumRank[0][1][0]]
        for i,j in sortNumRank[1:]:
            if j[0] in t:
                count += 1
        if count > 1:
            isDraw = True
            conflict = sortNumRank[:count]
            s_conflict = [i for x in suit_rank for i in conflict if i[1][1] == x]
            return isDraw, s_conflict[0]
        else:
            return isDraw, sortNumRank[0]

    def winner(self, sort_lst):
        """
            checks draw condition or winner
            param: sorted list of players(tuple) -> (key, name, indexOfkey)
            return: isDraw(bool), list of winner/draw
        """
        isDraw = False
        count = 0
        for k,n,i in sort_lst:
            if i == sort_lst[0][2]:
                count += 1
        if count >= 2:
            isDraw = True
            return isDraw, sort_lst[:count]
        else:
            return isDraw, sort_lst[0]

    def playerNames(self, n):
        player_list = []
        for i in range(n):
            player_list.append(input("enter player name: "))
        return player_list


if __name__ == '__main__':
    deck = Deck()
    hand = Hand()
    poker = Ranks()

    n = int(input("how many players want to play: "))
    player_names = poker.playerNames(n)
    deck.distribute_cards(2, player_names)                              # deal cards to players
    for name in player_names:
        hand.player_hand(deck, name, display=True)                      # display player's cards
    # hand.player_hand(deck, 'sabby', display=True)
    deck.move_cards('dealer', 5)                                        # deal dealer's cards
    hand.player_hand(deck, 'dealer', display=True)                      # display dealer's cards
    winner = poker.compare(player_names, hand, deck)                    # compares ranks of players
    print(winner)