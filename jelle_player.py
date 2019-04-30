from i_player import IPlayer
from card_set import CardSet


class JellePlayer(IPlayer):
    def __init__(self):
        self.hand=[]
        self.score=[0,0]
        self.update=False       #staat nu uit, vergeet niet ook announce score weer aan te zetten later
        self.bids=[]


    def give_hand(self, cards):
        self.hand=cards
        self.trick_score=[0,0,0,0]

        self.handlist=[0 for i in range(0,52)]          #list containing all the cards in the player's hand, not currently in use
        for i in range(0,len(self.hand)):
            self.handlist[self.hand[i].__int__()]=1

    def announce_bids(self, bids):
        self.bids=[0,0,0,0]

        for i in (0,1,2,3):
            self.bids[i]=bids[i]
            if bids[i] == "N":
                self.bids[i]=0



    def make_bid(self, bids):

        #The AI uses a text document called jelle-ai.txt to determine how valueable his hand is. Every card has value of it's own, but also influences the value of other cards of it's suit.
        #The AI adds up all modified values of the cards in it's hand and rounds it to the nearest integer.


        value_matrix=[[0,0,0,0,0,0,0,0,0,0,0,0,0] for i in range(4)] #this matrix is used to keep track of the expected value of the hand based on which cards are in it.

        ai_file = open("jelle-ai.txt", "r")                         #reads the source text file
        values=ai_file.readlines()
        ai_file.close()

        for cards_in_hand in range(0,13):                           #adjusts the value matrix. every card influences the value of other cards of it's suit.
            suit_id = self.hand[cards_in_hand].__int__() // 13
            number_id=self.hand[cards_in_hand].__int__() % 13
            if suit_id==0:
                for i in range(0,13):
                    value_matrix[0][i]=value_matrix[0][i]+float(values[(i+1)+number_id*14])
            else:
                for i in range(0,13):
                    value_matrix[suit_id][i]=value_matrix[suit_id][i]+float(values[(i+1)+number_id*14+182])

        total_value=0                                               #add up the value of all cards in the hand
        for cards_in_hand in range(0,13):
            suit_id = self.hand[cards_in_hand].__int__() // 13
            number_id = self.hand[cards_in_hand].__int__() % 13
            total_value+=value_matrix[suit_id][number_id]


        team_bid=bids.get_team_bid(0)[1]
        maximum_allowed_bid=13
        try:
            maximum_allowed_bid=13-team_bid
            self.update=False
        except:
            pass
        total_value=min(maximum_allowed_bid,max(1,total_value))

        #print(total_value)
        if total_value<2:
            return 0
        return round(total_value)                                   #return the rounded estimate of the value of the hand

    def play_card(self, trick, valid_cards):

        strategy = self.determine_strategy(trick,valid_cards)

        #print(trick)
        #print(valid_cards)
        #print("strategy:" + str(strategy))

        if strategy == "get rid of a good card" : #player is playing null and wants to get rid of good cards.
            if self.find_highest_losing_card_in_reaction(trick,valid_cards)!= None:
                return self.find_highest_losing_card_in_reaction(trick,valid_cards)
            return valid_cards.pop()

        if strategy == "get rid of a bad card" : #if team player seems to be winning the hand: play the lowest non-trick card available
            return self.find_card_to_get_rid_of(valid_cards)

        if strategy == "high opening":
            return self.find_high_card_to_open_with(trick,valid_cards)

        if strategy == "low opening":
            return self.find_low_card_to_open_with(trick,valid_cards)


        if strategy == "pop":
            return valid_cards.pop()

        if strategy=="play a strong winning card":
            return self.find_highest_winning_card_in_reaction(trick,valid_cards)

        if strategy=="play the lowest winning card":
            return self.find_lowest_winning_card(trick,valid_cards)




    def determine_strategy(self,trick,valid_cards):

        #check the game state, objectives and so on to determine what to do

        wants_to_win_more_tricks=True
        if self.bids[0] == 0 and self.trick_score[0] == 0:
            wants_to_win_more_tricks = False
        elif ((self.bids[0]+self.bids[2])<=(self.trick_score[0]+self.trick_score[2])) and ((self.bids[1]+self.bids[3])<=(self.trick_score[1]+self.trick_score[3])):
            #if the players team has enough tricks and the opponent has enough too, then attempt to lose
            wants_to_win_more_tricks = False

        #determine whether player can potentially win the trick
        able_to_win_trick=False
        opening=False
        if len(trick)==0:
            able_to_win_trick=True
            opening=True
        else:
            winner_id=trick.get_winner()
            for playable_cards in valid_cards:
                if playable_cards.__gt__(trick[winner_id]):
                    able_to_win_trick=True


        if len(trick)==3:
            last_to_act=True
        else:
            last_to_act = False

        #detirmine whether the player can be guaranteed to lose the trick
        guaranteed_to_lose_trick = False
        if len(trick)!=0:
            winner_id=trick.get_winner()
            for playable_cards in valid_cards:
                if trick[winner_id].__gt__(playable_cards):
                    guaranteed_to_lose_trick=True

        #print("wants to win more tricks: "+str(wants_to_win_more_tricks))
        #transform the observed game state into a strategy to play
        if opening and wants_to_win_more_tricks:
            return "high opening"
        if opening and not wants_to_win_more_tricks:
            return "low opening"

        if wants_to_win_more_tricks == False and guaranteed_to_lose_trick and not opening:
            return "get rid of a good card"

        if trick.get_winner()==2 and wants_to_win_more_tricks: #if team player seems to be winning the hand: play the lowest non-trick card available
            return "get rid of a bad card"

        if trick.get_winner()==2 and not wants_to_win_more_tricks: #if team player seems to be winning the hand: play the lowest non-trick card available
            return "get rid of a good card"

        if not opening and wants_to_win_more_tricks and able_to_win_trick and not last_to_act:
            return "play a strong winning card"

        if wants_to_win_more_tricks and last_to_act and able_to_win_trick:
            return "play the lowest winning card"

        if wants_to_win_more_tricks and not able_to_win_trick:
            return "get rid of a bad card"

        if not guaranteed_to_lose_trick and not wants_to_win_more_tricks and not opening:
            return "play the lowest winning card"

        print("no strat found")
        return "pop"


    def offer_blind_nill(self, bids):
        return False

    def receive_blind_nill_cards(self, cards):
        self.hand += cards

    def announce_score(self, score):
        #The AI decides whether to update how it estimates value of hands depending on the result of the round. If the AI did not reach it's intended amount of tricks, it adjusts the value
        #of the cards he had in his hand downwards. If the AI scored overtricks, he adjusts the value of his hand upwards.

        if self.update==True:
            if self.score[0]>score[0] and self.score[0] %10 == score[0] % 10:
                self.adjust_bet_value_downward()
            if self.score[0] %10 != score[0] % 10:
                self.adjust_bet_value_upwards()
        self.score=score
        self.update=False

    def announce_trick(self, trick):
        #print(trick)
        self.trick_score[trick.get_winner()]+=1

    def request_blind_nill_cards(self):
        offered_cards = self.hand[-2:]
        self.hand = self.hand[:-2]
        return offered_cards

    def adjust_bet_value_downward(self):
        ai_file=open("jelle-ai.txt","r")
        behaviour=ai_file.readlines()
        ai_file.close()

        current_hand=CardSet(self.hand)
        for i in ("S","H","C","D"):
            cards_sorted_by_suit=current_hand.get_suit_cards(i)
            if i == "S":
                for k in range(0,len(cards_sorted_by_suit)):
                    for j in range(0,len(cards_sorted_by_suit)):
                        k_card_index=(cards_sorted_by_suit[k].__int__()%13)*14
                        j_card_index=(cards_sorted_by_suit[j].__int__()%13)+1
                        behaviour[k_card_index+j_card_index]= float(behaviour[k_card_index+j_card_index])-0.01
            else:
                for k in range(0,len(cards_sorted_by_suit)):
                    for j in range(0,len(cards_sorted_by_suit)):
                        k_card_index=(cards_sorted_by_suit[k].__int__()%13)*14+182
                        j_card_index=(cards_sorted_by_suit[j].__int__()%13)+1
                        behaviour[k_card_index+j_card_index]= float(behaviour[k_card_index+j_card_index])-0.01

        ai_file=open("jelle-ai.txt","w")
        for i in range(0,len(behaviour)):
            try:
                behaviour[i]=float(behaviour[i])
                ai_file.write(str(behaviour[i]) + "\n")
            except:
                ai_file.write(behaviour[i])

        ai_file.close()

    def adjust_bet_value_upwards(self):
        ai_file = open("jelle-ai.txt", "r")
        behaviour = ai_file.readlines()
        ai_file.close()

        current_hand = CardSet(self.hand)
        for i in ("S", "H", "C", "D"):
            cards_sorted_by_suit = current_hand.get_suit_cards(i)
            if i == "S":
                for k in range(0, len(cards_sorted_by_suit)):
                    for j in range(0, len(cards_sorted_by_suit)):
                        k_card_index = (cards_sorted_by_suit[k].__int__() % 13) * 14
                        j_card_index = (cards_sorted_by_suit[j].__int__() % 13) + 1
                        behaviour[k_card_index + j_card_index] = float(behaviour[k_card_index + j_card_index]) + 0.01
            else:
                for k in range(0, len(cards_sorted_by_suit)):
                    for j in range(0, len(cards_sorted_by_suit)):
                        k_card_index = (cards_sorted_by_suit[k].__int__() % 13) * 14 + 182
                        j_card_index = (cards_sorted_by_suit[j].__int__() % 13) + 1
                        behaviour[k_card_index + j_card_index] = float(behaviour[k_card_index + j_card_index]) + 0.01

        ai_file = open("jelle-ai.txt", "w")
        for i in range(0, len(behaviour)):
            try:
                behaviour[i] = float(behaviour[i])
                ai_file.write(str(behaviour[i]) + "\n")
            except:
                ai_file.write(behaviour[i])

        ai_file.close()



    def find_highest_winning_card_in_reaction(self,trick,valid_cards):
            winnerid=trick.get_winner()
            best_card = trick[winnerid]
            for i in range(0, len(valid_cards)):
                if valid_cards[i].__gt__(best_card):
                    best_card = valid_cards[i]
            if best_card != trick[winnerid]:
                return best_card
            else: #there is no winning card

                return None


    def find_lowest_winning_card(self,trick,valid_cards):

        winnerid = trick.get_winner()
        best_card_in_trick = trick[winnerid]
        winning_cards = []
        for i in range(0, len(valid_cards)):
            if valid_cards[i].__gt__(best_card_in_trick):
                winning_cards.append(valid_cards[i])
        if len(winning_cards) > 0:
            best_card_to_play = winning_cards[0]
            for i in range(0, len(winning_cards)):
                if winning_cards[i].__int__() < best_card_to_play.__int__():
                    best_card_to_play = winning_cards[i]
            return best_card_to_play
        else:
            return None

    def find_highest_losing_card_in_reaction(self,trick, valid_cards):
        #returns None if there are no losing cards in valid-cards. Returns the highest card if all valid losing cards are of one suit. If there are more suits available in
        #the losing cards, then the AI will try to empty a suit.

        winning_player=trick.get_winner()
        winning_card_in_trick=trick[winning_player]

        losing_cards_in_hand=[]
        for i in range(0,len(valid_cards)):
            if winning_card_in_trick.__gt__(valid_cards[i]):
                losing_cards_in_hand.append(valid_cards[i])


        if len(losing_cards_in_hand)== 0:

            return None
        else:
            losing_cards_in_hand_cardset = CardSet(losing_cards_in_hand)
            for i in ("S","H","C","D"):
                if losing_cards_in_hand_cardset.get_suit_size(i)==len(losing_cards_in_hand): #there is only a single suit to choose from. Play the highest card of that suit.

                    highest_losing_card = losing_cards_in_hand[0]
                    for j in range(0,losing_cards_in_hand_cardset.get_suit_size(i)):
                        if losing_cards_in_hand[j].__gt__(highest_losing_card):
                            highest_losing_card=losing_cards_in_hand[j]

                    return highest_losing_card

                if losing_cards_in_hand_cardset.get_suit_size(i) == 1:
                    if losing_cards_in_hand_cardset.get_suit_cards(i)[
                        0].__int__() % 13 > 8:  # there is but a single high card of a suit, play it.

                        return losing_cards_in_hand_cardset.get_suit_cards(i)[0]

            if losing_cards_in_hand_cardset.get_suit_size("S") > 0:  # there is the option to get rid of a spades. The player chooses the highest spades available
                best_card_to_play = losing_cards_in_hand_cardset[0]
                for i in range(0,len(losing_cards_in_hand_cardset)):
                    if losing_cards_in_hand_cardset[i].__gt__(best_card_to_play):
                        best_card_to_play=losing_cards_in_hand_cardset[i]
                #print("spades available")
                return best_card_to_play

            #play the highest card
            best_card_to_play=losing_cards_in_hand_cardset[0]
            for i in range(0,len(losing_cards_in_hand_cardset)):
                if losing_cards_in_hand_cardset[i].__int__()%13 > best_card_to_play.__int__()%13:
                    best_card_to_play=losing_cards_in_hand_cardset[i]
            #print("high card")
            return best_card_to_play










    def find_low_non_trick_card(self,valid_cards):


        lowest_card = valid_cards[0]
        for i in range(1, len(valid_cards)):
            if lowest_card.__int__() / 13 == 0 and valid_cards[
                i].__int__() / 13 != 0:  # if the current low card is a trick and the following card is not, prefer the non-trick card
                lowest_card = valid_cards[i]
            if valid_cards[i].__int__() % 13 < lowest_card.__int__() % 13 and valid_cards[
                i].__int__() / 13 != 0:  # if the next card is lower that the current lowest, then the next card becomes the new lowest card, unless it is a trick card
                lowest_card = valid_cards[i]
            if valid_cards[i].__int__() % 13 == 0 and lowest_card.__int__() % 13 == 0:  # and lastly, if both are trick cards, then choose the lowest of the two
                if valid_cards[i].__int__() < lowest_card.__int__():
                    #print("check?")
                    lowest_card = valid_cards[i]
        return lowest_card

    def find_low_winning_trump_card(self,trick,valid_cards):

        valid_card_set=CardSet(valid_cards)
        trick_suit=trick.get_suit()
        current_winning_card=trick[trick.get_winner()]

        if trick_suit!="S" and valid_card_set.get_suit_size(trick_suit)==0 and valid_card_set.get_suit_size("S")>0 and current_winning_card.__int__()%13!=0: #if I don't have the requested suit and no other player has played spades
            worst_spades=valid_card_set.get_suit_cards("S")[0]
            for i in range(0,valid_card_set.get_suit_size("S")):
                if worst_spades.__gt__(valid_card_set.get_suit_cards("S")[i]):
                    worst_spades=valid_card_set.get_suit_cards("S")[i]
            return worst_spades

        if trick_suit != "S" and valid_card_set.get_suit_size(trick_suit) == 0 and valid_card_set.get_suit_size(
                "S") > 0 and current_winning_card.__int__() % 13 == 0:  # if I don't have the requested suit and another player has played spades
            better_trump_card_list=[]
            for i in range(0,len(valid_cards)):      #finds the better trump cards
                if valid_cards[i].__gt__(current_winning_card):
                    better_trump_card_list.append(valid_cards[i])
            if len(better_trump_card_list)>0:
                lowest_winning_trump=better_trump_card_list[0]
                for i in range(0,len(better_trump_card_list)):
                    if lowest_winning_trump.__gt__(better_trump_card_list[i]):
                        lowest_winning_trump=better_trump_card_list[i]
            else:
                return None


        return None



    def find_card_to_pull_out_trump_cards(self):
        pass

    def find_high_card_to_open_with(self,trick,valid_cards):
        best_card=valid_cards[0]
        for i in range(0,len(valid_cards)):
            if valid_cards[i].__int__()%13>best_card.__int__()%13:
                best_card=valid_cards[i]
        return best_card

    def find_low_card_to_open_with(self,trick,valid_cards):
        best_card=valid_cards[0]
        for i in valid_cards:
            if (i.__int__()%13)<(best_card.__int__()%13):
                best_card=i
        return best_card

    def find_card_to_get_rid_of(self,valid_cards):
        #Sometimes you can't win. That is an opportunity to get rid of an unwanted card. The AI will play the lowest card if he has only valid cards of a single suit.
        #If the AI has multiple suits to choose from and if he owns only a single low card of one of the non-trump suits, then he will play that card.
        #If the AI has multiple suits in his hand, but more cards of each suit, then he will play the lowest non-trump card available.

        valid_card_set=CardSet(valid_cards)
        for i in ("H","C","D"):
            if valid_card_set.get_suit_size(i)==len(valid_cards): #there is only one suit to choose from, choose the lowest card
                worst_card=valid_cards[0]
                for j in range(0,len(valid_cards)):
                    if worst_card.__gt__(valid_cards[j]):
                        worst_card=valid_cards[j]
                return worst_card
            else: #there are multiple suits in the valid_card_set

                if len(valid_card_set.get_suit_cards(i))==1: #if there is a single low non-trump card, get rid of it
                    if valid_card_set.get_suit_cards(i)[0].__int__()%13 <6:

                        return valid_card_set.get_suit_cards(i)[0]

            #just pick the lowest non trump card available
        return self.find_low_non_trick_card(valid_cards)