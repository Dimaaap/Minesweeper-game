import pytest

from game import *

list_colors = ['white', 'blue', 'green', 'yellow', 'purple', 'grey', 'black', 'red']


@pytest.mark.parametrize('number', list(range(8)))
def test_get_colors_by_count_mines(number):
    assert list_colors[number] == colors[number]


def test_get_colors_by_count_mines_button_text(create_button):
    assert colors[create_button] == list_colors[int(create_button)]


class TestTakeMines:
    mines_list = MinesMixin.take_mines(20)

    def test_excluding_number(self):
        assert 20 not in self.mines_list

    def test_valid_length(self):
        assert len(self.mines_list) == MyWindow.COUNT_MINES

    def test_raise_exception(self):
        with pytest.raises(ValueError):
            MinesMixin.take_mines('20')