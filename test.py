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
# def test_no_input():
#     """makes no input and use all defaults"""

#     rv, out = getstatusoutput(prg)
#     assert rv == 0
#     assert out.strip() == "Please input 4 digits as your guess (q to quit):"


# # --------------------------------------------------
# def test_bad_digits():
    """dies on bad digits"""

    expected = 'argument -d/--digits: invalid choice: {} (choose from 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'

    rv, out = getstatusoutput(f'{prg} --digits 13')
    assert rv != 0
    assert re.search(expected.format(13), out)


# # --------------------------------------------------
# def test_bad_times_str():
#     """dies on bad times string value"""

#     expected = "argument -t/--times: invalid int value: '{}'"

#     bad = random.choice(string.ascii_letters)
#     rv, out = getstatusoutput(f'{prg} --times {bad}')
#     assert rv != 0
#     assert re.search(expected.format(bad), out, re.I)


# # --------------------------------------------------
# def test_bad_seed():
#     """bad seed"""

#     bad = random_string()
#     rv, out = getstatusoutput(f'{prg} -s {bad}')
#     assert rv != 0
#     assert re.search(f"argument -s/--seed: invalid int value: '{bad}'", out)


# # --------------------------------------------------
# def random_string():
#     """generate a random filename"""

#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


# ###Set 2 to test number of A's and B's and answer###
# ###Not started yet###
# # --------------------------------------------------

