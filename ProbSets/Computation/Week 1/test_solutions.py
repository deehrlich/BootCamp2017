# test_solutions.py
"""Volume 1B: Testing.
<Name>
<Class>
<Date>
"""

import solutions as soln
import pytest
import math

# Problem 1: Test the addition and fibonacci functions from solutions.py
def test_addition():
    number_1, number_2, number_3, number_4 = 5,6,-3,-7
    assert number_1 + number_2  == soln.addition(5,6)
    assert number_3 + number_4  == soln.addition(-3,-7)
    assert number_1 + number_4 == soln.addition(5,-7)

def test_smallest_factor():
    number_1, number_2, number_3 = 1, 7, 10
    assert 1 == soln.smallest_factor(1)
    assert 7 == soln.smallest_factor(7)
    assert 2 == soln.smallest_factor(10)

# Problem 2: Test the operator function from solutions.py
def test_operator():
    number_1, number_2, number_3 = 3,5,0
    string_1, string_2, string_3, string_4, string_5, string_6 = '+', '/', '-', '*', 'ab', '%'

    with pytest.raises(Exception) as excinfo:
        soln.operator(number_1, number_2, number_3)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be a string"

    with pytest.raises(Exception) as excinfo:
        soln.operator(number_1, number_2, string_5)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be one character"

    assert number_1 + number_2 == soln.operator(number_1, number_2, string_1)
    assert number_1 / number_2 == soln.operator(number_1, number_2, string_2)

    with pytest.raises(Exception) as excinfo:
        soln.operator(number_1, number_3, string_2)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "You can't divide by zero!"

    assert number_1 - number_2 == soln.operator(number_1, number_2, string_3)
    assert number_1 * number_2 == soln.operator(number_1, number_2, string_4)

    with pytest.raises(Exception) as excinfo:
        soln.operator(number_1, number_3, string_6)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"

# Problem 3: Finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = soln.ComplexNumber(1, 2)
    number_2 = soln.ComplexNumber(5, 5)
    number_3 = soln.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == soln.ComplexNumber(6, 7)
    assert number_1 + number_3 == soln.ComplexNumber(3, 11)
    assert number_2 + number_3 == soln.ComplexNumber(7, 14)
    assert number_3 + number_3 == soln.ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == soln.ComplexNumber(-5, 15)
    assert number_1 * number_3 == soln.ComplexNumber(-16, 13)
    assert number_2 * number_3 == soln.ComplexNumber(-35, 55)
    assert number_3 * number_3 == soln.ComplexNumber(-77, 36)

def test_complex_subtraction(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 - number_2 == soln.ComplexNumber(-4, -3)
    assert number_1 - number_3 == soln.ComplexNumber(-1, -7)
    assert number_2 - number_3 == soln.ComplexNumber(3, -4)
    assert number_3 - number_3 == soln.ComplexNumber(0, 0)

def test_complex_division(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 / number_2 == soln.ComplexNumber(0.3, 0.1)
    assert number_1 / number_3 == soln.ComplexNumber(4/17, -1/17)
    assert number_2 / number_3 == soln.ComplexNumber(11/17, -7/17)
    assert number_3 / number_3 == soln.ComplexNumber(1, 0)

    with pytest.raises(Exception) as excinfo:
        number_1/ soln.ComplexNumber(0, 0)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Cannot divide by zero"

def test_complex_conjugate(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    print(number_1.conjugate().real, number_1.conjugate().imag)
    assert number_1.conjugate() == soln.ComplexNumber(1,-2)

def test_complex_eq(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert (number_1 == soln.ComplexNumber(1,2)) == True
    assert (number_1 == soln.ComplexNumber(1,3)) == False

def test_complex_norm(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_2.norm() == math.sqrt(50)

def test_complex_print(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert str(number_1) == "1+2i"

# Problem 4: Write test cases for the Set game.
def test_set():

    #test for valid set cards
    with pytest.raises(Exception) as excinfo:
        soln.set_game('hands/attribute_value.txt')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Card bit must be 0,1,2."

    with pytest.raises(Exception) as excinfo:
        soln.set_game('hands/attributes.txt')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Cards can only have 4 bits."

    #test for duplicate cards
    with pytest.raises(Exception) as excinfo:
        soln.set_game('hands/duplicates.txt')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "All cards must be unique."

    #test for number of cards
    with pytest.raises(Exception) as excinfo:
        soln.set_game('hands/12cards.txt')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Must have 12 cards."

    #test for file name
    with pytest.raises(Exception) as excinfo:
        soln.set_game('hands/fakefile.txt')
    assert excinfo.typename == 'FileNotFoundError'

    #test the final result
    assert soln.set_game('hands/correctgame.txt') == 6
