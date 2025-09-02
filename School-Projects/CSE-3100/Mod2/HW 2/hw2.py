import random

class Card:
    #initilizes the attributes of a card
    def __init__(self, number, color, shading, shape): 
        self.number = number
        self.color = color
        self.shading = shading
        self.shape = shape

    #access the card in string form using a magic method
    def __str__(self):
        return "Card(" + str(self.number) + ", " + self.color + ", " + self.shading + ", " + self.shape + ")"

    # we overided the method str(), so we use repr as str
    def __repr__(self): 
        return str(self)

    # checks string outputs for equality
    def __eq__(self, other): 
        return str(self) == str(other)


#declaring values for each group
number = [1, 2, 3]
color = ["green", "blue", "purple"]
shading = ["empty", "striped", "solid"]
shape = ["diamond", "squiggle", "oval"]


class Deck:
    def __init__(self, numbers = number, colors = color, shadings = shading, shapes = shape):
        #initilizing the deck
        self.my_deck = []
        
        self.number = numbers
        self.color = colors
        self.shading = shadings
        self.shape = shapes
        
        #Using nested loops to create all cards
        for a in numbers:
            for b in colors:
                for c in shadings:
                    for d in shapes:
                        card1 = Card(a, b, c, d)
                        self.my_deck.append(card1)

    # removes and returns top card
    def draw_top(self): 
        if (len(self.my_deck)==0):
            #if there are no cards, an attribute error is raised
            raise AttributeError
        else:
            return self.my_deck.pop()
        

    # Randomly shuffles a deck
    def shuffle(self): 
        random.shuffle(self.my_deck)

    # returns number of items in deck
    def __len__(self): 
        return len(self.my_deck)


def is_group(card1, card2, card3): 
    #Checks if all three attributes are all the same or all different. If so, we return true, otherwise we return false
    if(card1.number == card2.number and card1.number == card3.number) or (card1.number != card2.number and card1.number !=card3.number):
        if(card1.color == card2.color and card1.color == card3.color) or (card1.color != card2.color and card2.color != card3.color):
            if(card1.shading == card2.shading and card1.shading == card3.shading) or (card1.shading != card2.shading and card2.shading != card3.shading):
                if(card1.shape == card2.shape and card1.shape == card3.shape) or (card1.shape != card2.shape and card2.shape != card3.shape):
                    return True
                else:
                    return False
            else: 
                return False
        else:
            return False
    else:
        return False
