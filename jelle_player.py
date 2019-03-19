from i_player import IPlayer
import card

class JellePlayer(IPlayer):
    def __init__(self):
        self.hand=[]

    def give_hand(self, cards):
        self.hand=cards

        self.handlist=[0 for i in range(0,52)]
        for i in range(0,len(self.hand)):
            self.handlist[self.hand[i].__int__()]=1


    def make_bid(self, bids):

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
            total_value+=min(1,value_matrix[suit_id][number_id])



        return round(total_value)

    def play_card(self, trick, valid_cards):

        if trick.get_winner()==2 :              #if team player seems to be winning the hand: play a random card
            return valid_cards.pop()
        else:                                   #if an opposing player currently leads: play the best card available
            winnerid=trick.get_winner()
            if winnerid in (1,3):

                best_card=trick[winnerid]
                for i in range(0,len(valid_cards)):
                    if valid_cards[i].__gt__(best_card):
                        best_card=valid_cards[i]
                if best_card != trick[winnerid]:
                    return best_card


        return valid_cards.pop()                #If no player leads, then I won the last round and open with a random card

    def offer_blind_nill(self, bids):
        return False

    def receive_blind_nill_cards(self, cards):
        self.hand += cards

    def request_blind_nill_cards(self):
        offered_cards = self.hand[-2:]
        self.hand = self.hand[:-2]
        return offered_cards