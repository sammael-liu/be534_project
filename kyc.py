#!/usr/bin/env python3
"""
Author : wliu <wliu@localhost>
Date   : 2021-11-10
Purpose: Final Project
"""

import argparse
import random
import sys


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
                        default=5)

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed',
                        metavar='seed',
                        type=int,
                        default=None)

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

    answer = ''
    for ind in range(num_digits):
        answer += str(rand_ans[ind])
    # answer = ''
    # answer += [str(rand_ans[ind]) for ind in range(num_digits)]
    print(answer)

    user_input = get_input(num_digits)

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
        print('Guess number ' + str(times) + ': ' + str(count_a) + 'A' +
              str(count_b) + 'B')
        count_a = 0
        count_b = 0
        times += 1

        user_input = get_input(num_digits)

    print('Guess number ' + str(times) + ': ' + str(count_a) + 'A' +
          str(count_b) + 'B')

    if user_input == answer:
        print(
            'Congratulations! You made the correct guess and the answer is ' +
            answer + '.')
    else:
        print('Game Over! You already tried ' + str(args.times) +
              ' times and the answer is ' + answer + '.')


# --------------------------------------------------
def get_input(digits: int) -> str:
    """Check if user inputs: 
    (1) integer only 
    (2) the digits match to what they indicate in --digits"""

    prompt = f'Please input {str(digits)} digits as your guess (q to quit): '

    while True:
        user_input = input(prompt)
        if user_input.lower().startswith('q'):
            sys.exit('Player decided to quit the game!')

        if not user_input.isdigit():
            print(f'"{user_input}" is not a number')
            continue
        elif len(user_input) != digits:
            print(f'"{user_input}" is not {str(digits)} digits long')
            continue

    return user_input


# --------------------------------------------------
if __name__ == '__main__':
    main()
