import pytest

from ..mixins import MinesMixin
from ..game import colors

list_colors = ['white', 'blue', 'green', 'yellow', 'purple', 'grey', 'black', 'red']

parameters_for_test_take_mines_raises = [(2, 3, 5, '6'), (3, '', '', 5), ('', '', '', ''),
                                         (4, 5, 6, '')]
parameters_for_test_excluding_number = [(20, 10), (30, 5), (12, 21), (1, 10)]
parameters_for_minus_test = [(-3, -5), (3, 6), (1, -4), (34, 52)]
list_count_mines = list(range(7))


class TestTakeMines:

    @pytest.mark.parametrize('exclude_number, count_mines, rows, columns',
                             parameters_for_test_take_mines_raises)
    def test_take_mines_raises(self, exclude_number, count_mines, rows, columns):
        with pytest.raises(TypeError):
            MinesMixin.take_mines(exclude_number, count_mines, rows, columns)

    @pytest.mark.parametrize('exclude_number, count_mines', parameters_for_test_excluding_number)
    def test_excluding_number(self, exclude_number, count_mines):
        result = MinesMixin.take_mines(exclude_number, count_mines)
        assert exclude_number not in result

    @pytest.mark.parametrize('exclude_number, count_mines', parameters_for_test_excluding_number)
    def test_len_result(self, exclude_number, count_mines):
        result = MinesMixin.take_mines(exclude_number, count_mines)
        assert len(result) == count_mines

    @pytest.mark.parametrize('exclude_number, count_mines', parameters_for_minus_test)
    def test_minus_arguments(self, exclude_number, count_mines):
        result = MinesMixin.take_mines(exclude_number, count_mines)
        assert exclude_number not in result


class TestGetColorsByCountMines:

    def test_get_true_color(self, create_button):
        MinesMixin.get_colors_by_count_mines(create_button)
        assert create_button.is_open

    @pytest.mark.parametrize('count_mines', list_count_mines)
    def test_color_button_text(self, create_button, count_mines):
        create_button.count_mines = count_mines
        MinesMixin.get_colors_by_count_mines(create_button)
        assert create_button['disabledforeground'] == colors[create_button.count_mines]
