from Card import Deck, Hand


class Ranks(Hand):

    def __init__(self):
        Deck.__init__(self)
        Hand.__init__(self)
        self.playerTop5Cards = {}
        self.game = {}
        self.sortOrder = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6', '5', '4', '3', '2']
        self.suits = ['S', 'H', 'D', 'C']

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

    def isRoyalFlush(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        hist = self.histogram(final_player_hand)
        for count in hist.values():
            if count >= 5:
                key = list(hist.keys())[0]
                royal_flush = ['A'+ key, 'K'+ key, 'Q'+ key,'J'+ key, '0'+ key]
                if set(royal_flush).issubset(set(final_player_hand)):
                    if collect:
                        return royal_flush
                    else:
                        return True
        return False

    def isStraightFlush(self, fplyrCard, collect=False):

        flush = self.isFlush(fplyrCard)
        if flush:
            final_player_hand = fplyrCard
            hist = self.histogram(final_player_hand)
            for count in hist.values():
                if count >= 5:
                    suit = list(hist.keys())[0]
            if collect:
                cards = self.isStraight(fplyrCard, suits=[suit], collect=True)
                return cards
            else:
                straight = self.isStraight(fplyrCard, suits=[suit])
                return straight
        else:
            return False

    def isFlush(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        if collect:
            suitTemp = [i[1] for i in final_player_hand]
            for suit in self.suits:
                if suitTemp.count(suit) >= 5:
                    key = suit
                    break
            sortHand = [i for x in self.sortOrder for i in final_player_hand if i[0] == x]
            flush = []
            for card in sortHand:
                if card[1] == key:
                    if len(flush) == 5:
                        return flush
                    else:
                        flush.append(card[0])
        else:
            hist = self.histogram(final_player_hand)
            for count in hist.values():
                if count >= 5:
                    key = list(hist.keys())[0]
                    return True, key
            return False

    def isStraight(self, fplyrCard, suits=None, collect=False):

        suits = suits
        num   = ['A','K','Q','J','0','9','8','7','6','5','4','3','2','A']
        final_player_hand = fplyrCard
        if suits != None:
            for s in suits:
                count = 0
                temp = []
                for i in num:
                    card = i+s
                    if card in final_player_hand:
                        count += 1
                        if collect:
                            temp.append(card)
                            if count == 5:
                                return temp
                        if count == 5:
                            return True
                    else:
                        count = 0
                        temp = []

        else:
            only_num = [num[0] for num in final_player_hand]
            count = 0
            temp = []
            for i in num:
                if i in only_num:
                    count += 1
                    if collect:
                        temp.append(i)
                        if count == 5:
                            return temp
                    if count == 5:
                        return True
                else:
                    count = 0
                    temp = []
        return False

    def isFourOfKind(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        num = [i[0] for x in self.sortOrder for i in final_player_hand if i[0] == x]
        if collect:
            cards = []
            for card in num:
                if num.count(card) == 4:
                    cards.append(card)
                    if len(cards) == 4:
                        break
            for card in num:
                if card not in cards:
                    cards.append(card)
                    if len(cards) == 5:
                        break
            return cards
        else:
            for i in num:
                if num.count(i) >= 4:
                    return True
        return False

    def isFullHouse(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        num = [i[0] for i in final_player_hand]
        if collect:
            sortedCards = [i for x in self.sortOrder for i in num if i == x]
            fullHouse = []
            for card in sortedCards:
                if sortedCards.count(card) >= 3 and len(fullHouse)<3:
                    fullHouse.append(card)
            for card in sortedCards:
                if card not in fullHouse and sortedCards.count(card) >= 2 and len(fullHouse)<5:
                    fullHouse.append(card)
            return fullHouse
        else:
            for i in num:
                if num.count(i) >= 3:
                    temp = [j for j in num if j != i]
                    for elem in temp:
                        if temp.count(elem) >= 2:
                            return True
            return False

    def isThreeOfKind(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        num = [i[0] for i in final_player_hand]
        if collect:
            sortedCards = [i for x in self.sortOrder for i in num if i == x]
            threeOfKind = []
            for card in sortedCards:
                if sortedCards.count(card) >= 3 and len(threeOfKind) < 3:
                    threeOfKind.append(card)
            for card in sortedCards:
                if card not in threeOfKind and len(threeOfKind) < 5:
                    threeOfKind.append(card)
            return threeOfKind
        else:
            for i in num:
                if num.count(i) >= 3:
                    return True
            return False

    def isTwoOfKind(self, fplyrCard, collect=False):  # two pair

        final_player_hand = fplyrCard
        num = [i[0] for i in final_player_hand]
        if collect:
            sortedCards = [i for x in self.sortOrder for i in num if i == x]
            twoPair = []
            for i in sortedCards:
                if sortedCards.count(i) >= 2 and len(twoPair) < 4:
                    twoPair.append(i)
            for i in sortedCards:
                if i not in twoPair and len(twoPair) < 5:
                    twoPair.append(i)
            return twoPair
        else:
            for i in num:
                if num.count(i) >= 2:
                    temp = [j for j in num if j != i]
                    for elem in temp:
                        if temp.count(elem) >= 2:
                            return True
            return False

    def isPair(self, fplyrCard, collect=False):

        final_player_hand = fplyrCard
        num = [i[0] for x in self.sortOrder for i in final_player_hand if i[0] == x]
        if collect:
            pair = []
            for i in num:
                if num.count(i) > 1:
                    pair.append(i)
                    if len(pair) == 2:
                        break
            for i in num:
                if i not in pair:
                    pair.append(i)
                    if len(pair) == 5:
                        break
            return pair
        else:
            for i in num:
                if num.count(i) >= 2:
                    return True
            return False

    def highCard(self, fplyrCard):

        final_player_hand = fplyrCard
        sort_order = ['A','K','Q','J','0','9','8','7','6','5','4','3','2']
        suit_rank = ['S','H','D','C']
        res = [i for x in sort_order for i in final_player_hand if i[0] == x]
        count = 1
        t = [res[0][0]]
        for i in res[1:]:
            if i[0] in t:
                count += 1
        if count > 1:
            conflict = res[:count]
            s_conflict = [i for x in suit_rank for i in conflict if i[1] == x]
            return s_conflict[0]
        else:
            return res[0]
    def compare(self, player_names, player_dict):

        #game = {}
        for name in player_names:
            rank_res = {}
            fplyrCards = player_dict[name]
            rank_res.update(RoyalFlush = poker.isRoyalFlush(fplyrCards))
            rank_res.update(StraightFlush = poker.isStraightFlush(fplyrCards))
            rank_res.update(FourOfKind = poker.isFourOfKind(fplyrCards))
            rank_res.update(FullHouse= poker.isFullHouse(fplyrCards))
            rank_res.update(Flush = poker.isFlush(fplyrCards))
            rank_res.update(Straight = poker.isStraight(fplyrCards))
            rank_res.update(ThreeOfKind= poker.isThreeOfKind(fplyrCards))
            rank_res.update(TwoPair = poker.isTwoOfKind(fplyrCards))  # two pair
            rank_res.update(Pair = poker.isPair(fplyrCards))
            rank_res.update(highCard = poker.highCard(fplyrCards))
            self.game[name] = rank_res
        lst = []
        for name in player_names:
            index = 1
            for key, val in self.game[name].items():
                if val == True:
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
                print(self.game[name].get('highCard'), -1)
                highCard_list.append((name, self.game[name]['highcard']))
            isDraw, res = self.draw(highCard_list)
            return f"{res[0]} won with {res[1]} high card"

    def draw(self, listOfTuple):                            # list = list of tuple(name, highcard)
        isDraw = False
        num_rank= ['A','K','Q','J','0','9','8','7','6','5','4','3','2']
        suit_rank = ['S','H','D','C']
        sortNumRank = [i for x in num_rank for i in listOfTuple if i[1][0] == x]
        count = 1
        t = [sortNumRank[0][1][0]]
        for i,j in sortNumRank[1:]:
            if j[0] in t:
                count += 1
        if count > 1:
            isDraw = True
            conflict = sortNumRank[:count]
            s_conflict = [i for x in suit_rank for i in conflict if i[1][1] == x]
            temp = [s_conflict[0][1]]
            flag = 0
            for i, j in s_conflict[1:]:
                if j in temp:
                    flag += 1
            if flag == 0:
                return isDraw, s_conflict[0]
            else:
                print('high card draw checking second high card')
                names = [name[0] for name in s_conflict]
                res = self.highCardAllPlayers(names)
                noUse, winner = self.draw(list(res.items()))
                return winner
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
            tieList = sort_lst[:count]
            isDraw, tieWinner = self.tieBreaker(tieList)
            return isDraw, tieWinner
        else:
            return isDraw, sort_lst[0]

    def tieBreaker(self, sort_list):
        '''
        fires when rank draw comes up and implements tie breaker acc to rank
        :param sort_list: [(key, name, indexOfKey)] only of players with tie
        :return: isDraw, list of draw OR winner(key, name, indexOfKey)
        '''
        print('in tie breaker')
        playernames = [name for k, name, i in sort_list]
        player_dict = self.finalPlayerHandList(playernames)
        self.collectCards(sort_list, player_dict)

        if sort_list[0][0] == 'RoyalFlush':
            isDraw = False
            cards = list(self.playerTop5Cards.values())
            count = 0
            dealer = player_dict['dealer']
            for i in cards:
                if i in dealer:
                    count += 1
                else:
                    count = 0
            if count == len(sort_list):
                isDraw = True
                return isDraw, sort_list
            else:
                """ only runs when total cards or more than 7 """
                t = list(self.playerTop5Cards.items())
                suits = ['S', 'H', 'D', 'C']
                sort_t = [(name,card) for x in suits for name,card in t if card[0][1] == x]
                winner_name = sort_t[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return isDraw, tup

        elif sort_list[0][0] == 'StraightFlush':
            temp = list(self.playerTop5Cards.items())
            res = [(name,cards) for x in self.sortOrder for name,cards in temp if cards[-1][0] == x]
            winner_name = res[0][0]
            for tup in sort_list:
                if tup[1] == winner_name:
                    return False, tup

        elif sort_list[0][0] == 'FourOfKind':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[1] == x]
            isDraw, win = self.isDuplicate(res, res[0][1], index=0)
            if isDraw:
                isDraw, win = self.isDuplicate(win, win[0][1], index=-1)
                if isDraw:
                    drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                    return True, drawlist
                else:
                    sort = [(name, cards) for x in self.sortOrder for name, cards in win if cards[-1] == x]
                    return False, sort[0]
            else:
                winner_name = win[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

        elif sort_list[0][0] == 'FullHouse':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[0] == x]
            isDraw, win = self.isDuplicate(res, res[0][1][0], index=0)
            if isDraw:
                n = 3
                while True:
                    if n == 4 and isDraw:
                        print('draw')
                        drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                        return True, drawlist
                    elif isDraw:
                        isDraw, win = self.pairTieBreaker(win, n)
                        n += 1
                    else:
                        winner_name = win[0][0]
                        for tup in sort_list:
                            if tup[1] == winner_name:
                                return False, tup
            else:
                winner_name = win[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

        elif sort_list[0][0] == 'Flush':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[0] == x]
            isDraw, win = self.isDuplicate(res, res[0][1][0], index=0)
            if isDraw:
                n = 1
                while True:
                    if n == 5 and isDraw:
                        print('draw')
                        drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                        return True, drawlist
                    elif isDraw:
                        isDraw, win = self.isDuplicate(win, win[0][1][n], index=n)
                        n += 1
                    else:
                        winner_name = win[0][0]
                        for tup in sort_list:
                            if tup[1] == winner_name:
                                return False, tup
            else:
                winner_name = win[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup


        elif sort_list[0][0] == 'Straight':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[1] == x]
            isDraw, win = self.isDuplicate(res, res[0][1])
            if isDraw:
                drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                return True, drawlist
            else:
                winner_name = res[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

        elif sort_list[0][0] == 'ThreeOfKind':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[0] == x]
            isDraw, win = self.isDuplicate(res, res[0][1][0], index=0)
            if isDraw:
                n = 3
                while True:
                    if n > 4 and isDraw:
                        print('draw')
                        drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                        return True, drawlist
                    elif isDraw:
                        isDraw, win = self.pairTieBreaker(win, n)
                        n += 1
                    else:
                        winner_name = win[0][0]
                        for tup in sort_list:
                            if tup[1] == winner_name:
                                return False, tup
            else:
                winner_name = win[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

        elif sort_list[0][0] == 'TwoPair':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[0] == x]
            isDraw, win = self.isDuplicate(res, res[0][1][0], index=0)
            if isDraw:
                n = 2
                while True:
                    if n > 5 and isDraw:
                        print('draw')
                        drawlist = [tup for x in win for tup in sort_list if tup[1] == x[0]]
                        return True, drawlist
                    elif isDraw:
                        isDraw, win = self.pairTieBreaker(win, n)
                        n += 2
                    else:
                        winner_name = win[0][0]
                        for tup in sort_list:
                            if tup[1] == winner_name:
                                return False, tup
            else:
                winner_name = win[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

        elif sort_list[0][0] == 'Pair':
            temp = list(self.playerTop5Cards.items())
            res = [(name, cards) for x in self.sortOrder for name, cards in temp if cards[0] == x]
            target = res[0][1][0]
            bool, l = self.isDuplicate(res, target, index=0)
            if bool:
                n = 2
                while True:
                    if n == 5 and bool:
                        print('draw')
                        drawlist = [tup for x in l for tup in sort_list if tup[1] == x[0]]
                        return True, drawlist
                    elif bool:
                        bool, l = self.pairTieBreaker(l, n)
                        n += 1
                    else:
                        winner_name = l[0][0]
                        for tup in sort_list:
                            if tup[1] == winner_name:
                                return False, tup
            else:
                winner_name = l[0][0]
                for tup in sort_list:
                    if tup[1] == winner_name:
                        return False, tup

    def pairTieBreaker(self, l, n):
        #temp = list(self.playerTop5Cards.items())
        res = [(name, cards) for x in self.sortOrder for name, cards in l if cards[n] == x]
        bool, ans = self.isDuplicate(res, res[0][1][n], index=n)
        return bool, ans

    def isDuplicate(self, ls, target, index=None):
        count = 0
        for name, cards in ls[1:]:
            if index != None:
                if len(set(target).difference(set(cards[index]))) == 0:
                    count += 1
            else:
                if len(set(target).difference(set(cards))) == 0:
                    count += 1
        if count >= 1:
            return True, ls[:count+1]
        else:
            return False, ls


    def collectCards(self, sort_list, player_dict):
        '''
        :param: sort_list, player_dict: [(key, name, indexOfKey)], {name: [7 cards]} only of players with tie
        :return: top5: {name: [best 5 cards of player]}
        '''
        for key, name, i in sort_list:
            fplyrCard = player_dict[name]
            if key == 'RoyalFlush':
                self.playerTop5Cards[name] = self.isRoyalFlush(fplyrCard, collect=True)

            elif key == 'StraightFlush':
                self.playerTop5Cards[name] = self.isStraightFlush(fplyrCard, collect=True)

            elif key == 'FourOfKind':
                self.playerTop5Cards[name] = self.isFourOfKind(fplyrCard, collect=True)

            elif key == 'FullHouse':
                self.playerTop5Cards[name] = self.isFullHouse(fplyrCard, collect=True)

            elif key == 'Flush':
                self.playerTop5Cards[name] = self.isFlush(fplyrCard, collect=True)

            elif key == 'Straight':
                self.playerTop5Cards[name] = self.isStraight(fplyrCard, collect=True)

            elif key == 'ThreeOfKind':
                self.playerTop5Cards[name] = self.isThreeOfKind(fplyrCard, collect=True)

            elif key == 'TwoPair':
                self.playerTop5Cards[name] = self.isTwoOfKind(fplyrCard, collect=True)

            elif key == 'Pair':
                self.playerTop5Cards[name] = self.isPair(fplyrCard, collect=True)

            else:
                print('not yet collected')

    def playerNames(self, n):
        player_list = []
        for i in range(n):
            name = input("enter player name: ")
            while True:
                if name in player_list or name == "":
                    print("INVALID NAME / NAME ALREADY TAKEN")
                    name = input("enter player name: ")
                else:
                    player_list.append(name)
                    break
        return player_list


if __name__ == '__main__':

    poker = Ranks()
    while True:
        n = int(input("how many players want to play: "))
        if n > 23:
            print()
            print("we only have 52 cards please reduce the no. of players playing")
            print()
        else:
            break
    player_names = poker.playerNames(n)
    print()
    poker.distribute_cards(2, player_names)                             # deal cards to players
    print()
    for name in player_names:
        poker.player_hand(hand=name, display=True)                      # display player's cards
    poker.move_cards('dealer', 5)                                       # deal dealer's cards
    poker.player_hand(hand='dealer', display=True)                      # display dealer's cards
    finalPlayerHand_dict = poker.finalPlayerHandList(player_names)
    winner = poker.compare(player_names, finalPlayerHand_dict)          # compares ranks of players
    print(winner)