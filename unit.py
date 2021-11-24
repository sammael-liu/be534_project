from unittest import mock
from unittest import TestCase
from project import get_input

def test_get_input():
    """Test get_input"""

    with mock.patch.object(__builtins__, 'input', lambda _: '123'):
        assert get_input(4) == 'Error! "123" is not 4 digits long'