# solutions.py
"""Volume IB: Testing.
<Name>
<Date>
"""
import math
import itertools
from collections import Counter

# Problem 1 Write unit tests for addition().
# Be sure to install pytest-cov in order to see your code coverage change.


def addition(a, b):
    return a + b


def smallest_factor(n):
    """Finds the smallest prime factor of a number.
    Assume n is a positive integer.
    """
    if n == 1:
        return 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return n


# Problem 2 Write unit tests for operator().
def operator(a, b, oper):
    if type(oper) != str:
        raise ValueError("Oper should be a string")
    if len(oper) != 1:
        raise ValueError("Oper should be one character")
    if oper == "+":
        return a + b
    if oper == "/":
        if b == 0:
            raise ValueError("You can't divide by zero!")
        return a/float(b)
    if oper == "-":
        return a-b
    if oper == "*":
        return a*b
    else:
        raise ValueError("Oper can only be: '+', '/', '-', or '*'")

# Problem 3 Write unit test for this class.
class ComplexNumber(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def norm(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real, imag)

    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real, imag)

    def __mul__(self, other):
        real = self.real*other.real - self.imag*other.imag
        imag = self.imag*other.real + other.imag*self.real
        return ComplexNumber(real, imag)

    def __truediv__(self, other):
        if other.real == 0 and other.imag == 0:
            raise ValueError("Cannot divide by zero")
        bottom = (other.conjugate()*other*1.).real
        top = self*other.conjugate()
        return ComplexNumber(top.real / bottom, top.imag / bottom)

    def __eq__(self, other):
        return self.imag == other.imag and self.real == other.real

    def __str__(self):
        return "{}{}{}i".format(self.real, '+' if self.imag >= 0 else '-',
                                                                abs(self.imag))

# Problem 5: Write code for the Set game here
def set_game(filename):
    with open(filename, 'r') as infile:
        lines = infile.readlines()

    cards = convert_to_array(lines)
    validate_set(cards)
    numset = find_match(cards)
    print("The Number of Matches is: ", numset)
    return numset

def convert_to_array(lines):
    cards=[]
    lines = [x.strip() for x in lines]
    for line in lines:
        card = [int(d) for d in line]
        cards.append(card)
    return cards

def find_match(cards):
    match = 0
    for triple in itertools.combinations(cards,3):
        colsum = [sum(x) for x in zip(*triple)]
        if all(i%3 ==0 for i in colsum):
            match += 1
    return match

def validate_set(cards):

    for card in cards:
        if len(card) != 4:
            raise ValueError("Cards can only have 4 bits.")
        for i in range(4):
            if card[i] != 0 and card[i] != 1 and card[i] != 2:
                raise ValueError("Card bit must be 0,1,2.")

    if len(cards) != 12:
        raise ValueError("Must have 12 cards.")

    unique = [list(x) for x in set(tuple(x) for x in cards)]
    if len(unique) != len(cards):
            raise ValueError("All cards must be unique.")
