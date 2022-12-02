import pytest

from ..game import MenuCommands, MyWindow


@pytest.mark.parametrize('rows, columns', [(20, 20),
                                           (10, 30),
                                           (59, 59),
                                           (15, 15)])
def test_check_input_values_valid(rows, columns):
    input_values = MenuCommands.check_input_values(rows, columns)
    assert input_values is None


@pytest.mark.parametrize('rows, columns', [(2, 2),
                                           (0, 0),
                                           (61, 61),
                                           (100, 5),
                                           (4, 32),
                                           (64, 20)
                                           ])
@pytest.mark.xfail
def test_check_input_values_invalid(rows, columns):
    input_values = MenuCommands.check_input_values(rows, columns)
    assert input_values is None


@pytest.mark.parametrize('count, value', [
    (20, 30),
    (5, 6),
    (10, (MyWindow.ROWS * MyWindow.COLUMNS) * 5),
    (0, 40)
])
def test_check_count_mines_valid(count, value):
    assert count < value


@pytest.mark.parametrize('count, value', [
    (30, 30),
    (25, 25),
    (0, 0),
    (1, 0),
    (45, 50)
])
@pytest.mark.xfail
def test_check_count_mines_invalid(count, value):
    assert count < value
