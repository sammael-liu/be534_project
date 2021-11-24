#!/usr/bin/env python3
"""
Author : wliu <wliu@localhost>
Date   : 2021-11-10
Purpose: Final Project
"""

import argparse
import random
import sys
from collections import Counter
from typing import Tuple


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='''BE534 Final Project - 1A2B Game\n
The program will create a random 4-digit secret number and the digits will all be different. (Four is the default value, but you can change it in the game setting.) The player needs to guess this number, and the program will give the clues while the player is guessing. If the matching digits are in the right positions, the program will treat them as "A", if in different positions, the program will treat them as "B". For example:\n
* Random secret number generated by the program: 1234\n
* The player's guess: 0213\n
* The clues from the program: 1A2B\n
One "A" is from the digit 2 in the right position, and two "B" are from 1 and 3 that they are in the number but in the different positions.''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-d',
                        '--digits',
                        help='Number of digits to play, default=4',
                        metavar='digits',
                        type=int,
                        choices=range(1, 11),
                        default=4)

    parser.add_argument('-t',
                        '--times',
                        help='Number of guesses allowed, default=10',
                        metavar='times',
                        type=int,
                        default=10)

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed, default=None',
                        metavar='seed',
                        type=int,
                        default=None)

    parser.add_argument(
        '-a',
        '--answer',
        help='Answer used for test, the player can ignore this argument',
        metavar='STR')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    random.seed(args.seed)
    num_digits = args.digits

    numbers = list(range(10))
    rand_ans = []
    for _i in range(num_digits):
        ind_choose = random.choice(numbers)
        rand_ans.append(ind_choose)
        numbers.remove(ind_choose)

    answer = ''.join([str(rand_ans[ind]) for ind in range(num_digits)])
    # print(answer)

    user_input = args.answer or get_input(num_digits)

    count_a = 0
    count_b = 0
    times = 1
    while times < args.times and user_input != answer:
        for user_ind in range(num_digits):
            for ans_ind in range(num_digits):
                if user_ind == ans_ind and user_input[user_ind] == answer[
                        ans_ind]:
                    count_a += 1
                elif user_input[user_ind] == answer[ans_ind]:
                    count_b += 1
        print(f'Guess number {times}: {count_a}A{count_b}B')
        count_a = 0
        count_b = 0
        times += 1

        user_input = get_input(num_digits)

    if user_input == answer:
        print(
            f'Congratulations! You made the correct guess and the answer is {answer}.'
        )
    else:
        print(
            f'Game Over! You already tried {args.times} times and the answer is {answer}.'
        )


# --------------------------------------------------
def get_input(digits: int) -> str:
    """Check if user inputs: 
    (1) integer only 
    (2) the digits match to what they indicate in --digits
    (3) cannot have duplicates"""

    prompt = f'Please input {str(digits)} digits as your guess (q to quit): '

    while True:
        user_input = input(prompt)
        if user_input.lower().startswith('q'):
            sys.exit('Player decided to quit the game!')

        checked, error = check_input(digits, user_input)

        if error:
            print(error)
        else:
            return checked


# --------------------------------------------------
def check_input(digits: int, value: str) -> Tuple[str, str]:
    """
    Check input from user
    Upon success, return (valid input, None)
    Upone failure, return (None, error message)
    """

    if not value.isdigit():
        return ('', f'Error! "{value}" is not a number')

    if len(value) != digits:
        return ('', f'Error! "{value}" is not {digits} digits long')

    if len(list(Counter(value).values())) != digits:
        return ('', f'Error! There are duplicate digits in "{value}"')

    return (value, '')


# --------------------------------------------------
def test_check_input():
    """ Test check_input """

    assert check_input(4, 'foo') == ("", 'Error! "foo" is not a number')
    assert check_input(4, '1') == ("", 'Error! "1" is not 4 digits long')
    assert check_input(
        4, '2112') == ("", 'Error! There are duplicate digits in "2112"')
    assert check_input(4, '1234') == ('1234', "")


# --------------------------------------------------
if __name__ == '__main__':
    main()
