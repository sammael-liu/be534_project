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
from unittest import mock
import sys
from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch
from typing import Optional


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Final Project',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d',
                        '--digits',
                        help='Number of digits to play',
                        metavar='digits',
                        type=int,
                        choices=range(1, 11),
                        default=4)

    parser.add_argument('-t',
                        '--times',
                        help='Number of guesses allowed',
                        metavar='times',
                        type=int,
                        default=10)

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed',
                        metavar='seed',
                        type=int,
                        default=None)

    parser.add_argument('-a',
                        '--answer',
                        help='Answer',
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
    print(answer)

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

    print(f'Guess number {times}: {count_a}A{count_b}B')

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

        user_input, error = check_input(digits, user_input)

        if error:
            print(error)
        else:
            return user_input


# --------------------------------------------------
def check_input(digits: int, value: str) -> (Optional[str], Optional[str]):
    """
    Check input from user
    Upon success, return (valid input, None)
    Upone failure, return (None, error message)
    """

    if not value.isdigit():
        return (None, f'Error! "{value}" is not a number')

    if len(value) != digits:
        return (None, f'Error! "{value}" is not {digits} digits long')

    if len(list(Counter(value).values())) != digits:
        return (None, f'Error! There are duplicate digits in "{values}"')

    return (value, None)


# --------------------------------------------------
def test_check_input():
    """ Test check_input """

    assert check_input(4, 'foo') == (None, 'Error! "foo" is not a number')
    assert check_input(4, '1') == (None, 'Error! "123" is not 4 digits long')
    assert check_input(
        4, '2112') == (None, 'Error! There are duplicate digits in "2112"')
    assert check_input(4, '1234') == ('1234', None)


# --------------------------------------------------
if __name__ == '__main__':
    main()
