#!/usr/bin/env python3
"""tests for project.py"""

from subprocess import getstatusoutput, getoutput
import os
import random
import re
import string

prg = './project.py'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


### Set 1 to test argparse input###
# --------------------------------------------------
def test_no_input():
    """makes no input and use all defaults"""

    rv, out = getstatusoutput(prg)
    assert rv == 0
    assert out.strip() == "Please input 4 digits as your guess (q to quit):"


# --------------------------------------------------
def test_bad_digits():
    """dies on bad digits"""

    expected = 'argument -d/--digits: invalid choice: {} (choose from 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'

    for bad in ['12', '0']:
        rv, out = getstatusoutput(f'{prg} --digits {bad}')
        assert rv != 0
        assert re.search(expected.format(bad), out)


# --------------------------------------------------
def test_bad_times_str():
    """dies on bad times string value"""

    expected = "argument -t/--times: invalid int value: '{}'"

    bad = random.choice(string.ascii_letters)
    rv, out = getstatusoutput(f'{prg} --times {bad}')
    assert rv != 0
    assert re.search(expected.format(bad), out, re.I)


# --------------------------------------------------
def test_bad_seed():
    """bad seed"""

    bad = random_string()
    rv, out = getstatusoutput(f'{prg} -s {bad}')
    assert rv != 0
    assert re.search(f"argument -s/--seed: invalid int value: '{bad}'", out)


# --------------------------------------------------
def random_string():
    """generate a random filename"""

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


###Set 2 to test number of A's and B's and answer###
###Not started yet###
# --------------------------------------------------
def test_both_player_and_cell():
    """test for both --player and --cell"""

    player = random.choice('XO')
    rv, out = getstatusoutput(f'{prg} --player {player}')
    assert rv != 0
    assert re.search('Must provide both --player and --cell', out)


# --------------------------------------------------
def test_good_board_01():
    """makes board on good input"""

    board = """
-------------
| 1 | 2 | 3 |
-------------
| 4 | 5 | 6 |
-------------
| 7 | 8 | 9 |
-------------
No winner.
""".strip()

    rv, out = getstatusoutput(f'{prg} -b .........')
    assert rv == 0
    assert out.strip() == board


# --------------------------------------------------
def test_good_board_02():
    """makes board on good input"""

    board = """
-------------
| 1 | 2 | 3 |
-------------
| O | X | X |
-------------
| 7 | 8 | 9 |
-------------
No winner.
""".strip()

    rv, out = getstatusoutput(f'{prg} --board ...OXX...')
    assert rv == 0
    assert out.strip() == board


# --------------------------------------------------
def test_mutate_board_01():
    """mutates board on good input"""

    board = """
-------------
| X | 2 | 3 |
-------------
| 4 | 5 | 6 |
-------------
| 7 | 8 | 9 |
-------------
No winner.
""".strip()

    rv, out = getstatusoutput(f'{prg} -b ......... --player X -c 1')
    assert rv == 0
    assert out.strip() == board


# --------------------------------------------------
def test_mutate_board_02():
    """mutates board on good input"""

    board = """
-------------
| X | X | O |
-------------
| 4 | O | 6 |
-------------
| O | O | X |
-------------
O has won!
""".strip()

    rv, out = getstatusoutput(f'{prg} --board XXO...OOX --p O -c 5')
    assert rv == 0
    assert out.strip() == board


# --------------------------------------------------
def test_mutate_cell_taken():
    """test for a cell already taken"""

    rv1, out1 = getstatusoutput(f'{prg} -b XXO...OOX --player X --cell 9')
    assert rv1 != 0
    assert re.search('--cell "9" already taken', out1)

    rv2, out2 = getstatusoutput(f'{prg} --board XXO...OOX --p O -c 1')
    assert rv2 != 0
    assert re.search('--cell "1" already taken', out2)


# --------------------------------------------------
def test_winning():
    """test winning boards"""

    wins = [('PPP......'), ('...PPP...'), ('......PPP'), ('P..P..P..'),
            ('.P..P..P.'), ('..P..P..P'), ('P...P...P'), ('..P.P.P..')]

    for player in 'XO':
        other_player = 'O' if player == 'X' else 'X'

        for board in wins:
            board = board.replace('P', player)
            dots = [i for i in range(len(board)) if board[i] == '.']
            mut = random.sample(dots, k=2)
            test_board = ''.join([
                other_player if i in mut else board[i]
                for i in range(len(board))
            ])
            out = getoutput(f'{prg} -b {test_board}').splitlines()
            assert out[-1].strip() == f'{player} has won!'


# --------------------------------------------------
def test_losing():
    """test losing boards"""

    losing_board = list('XXOO.....')
    for i in range(10):
        random.shuffle(losing_board)
        out = getoutput(f'{prg} -b {"".join(losing_board)}').splitlines()
        assert out[-1].strip() == 'No winner.'
