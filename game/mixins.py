from random import shuffle


colors = {0: 'white', 1: 'blue', 2: 'green', 3: 'yellow', 4: 'purple', 5: 'grey', 6: 'black',
          7: 'red',
          }


class MinesMixin:

    def get_mines(self, button_number: int, buttons: list, count_mines,
                  rows: int = 10, columns: int = 10):
        numbers_list = self.take_mines(button_number, count_mines, rows, columns)
        for row_buttons in range(1, rows + 1):
            for button in range(1, columns + 1):
                btn = buttons[row_buttons][button]
                if btn.number in numbers_list:
                    btn.IS_MINE = True

    @staticmethod
    def show_all_mines(buttons, rows: int = 10, columns: int = 10):
        for i in range(1, rows + 1):
            for j in range(1, columns + 1):
                button = buttons[i][j]
                if button.IS_MINE:
                    button['text'] = '*'
                    button.config(text='*')

    @staticmethod
    def get_colors_by_count_mines(button: callable):
        color = colors[button.count_mines]
        button.config(text=button.count_mines, disabledforeground=color)
        if not button.is_open:
            button.is_open = True

    @staticmethod
    def take_mines(exclude_number: int, count_mines, rows: int = 10, columns: int = 10):
        numbers_list = list(range(1, rows * columns + 1))
        numbers_list.remove(exclude_number)
        shuffle(numbers_list)
        return numbers_list[:count_mines]
