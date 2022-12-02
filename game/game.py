import tkinter as tk
from tkinter.messagebox import showinfo, showerror

from .buttons import MyButton
from .mixins import MinesMixin

colors = {0: 'white', 1: 'blue', 2: 'green', 3: 'yellow', 4: 'purple', 5: 'grey', 6: 'black',
          7: 'red',
          }


class MyWindow(MyButton, MinesMixin):
    ROWS = 10
    COLUMNS = 10
    COUNT_MINES = int(ROWS * COLUMNS * 0.2)
    win = tk.Tk()
    POSSIBLE_COORDINATE_CHOICE = (-1, 0, 1)
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(MyWindow.ROWS + 2):
            temp_list = []
            for j in range(MyWindow.COLUMNS + 2):
                button = MyButton(MyWindow.win, x=i, y=j)
                button.config(command=lambda btn=button: self.click_button(btn,
                                                                           MyWindow.IS_GAME_OVER,
                                                                           MyWindow.IS_FIRST_CLICK
                                                                           ))
                button.bind("<Button-3>", self.right_click)
                temp_list.append(button)
            self.buttons.append(temp_list)

    @staticmethod
    def right_click(event):
        if MyWindow.IS_GAME_OVER:
            return
        current_button = event.widget
        if current_button['state'] == 'normal':
            current_button['state'] = 'disabled'
            current_button['text'] = '🚩'
            current_button['disabledforeground'] = 'red'
        elif current_button['text'] == '🚩':
            current_button['text'] = ''
            current_button['state'] = 'normal'

    def button_is_mine(self, button: callable):
        button.config(text='*', background='red', disabledforeground='black')
        button.is_open = True
        MyWindow.IS_GAME_OVER = True
        showinfo('Game Over!', 'Ви програли')
        self.show_all_mines(self.buttons, MyWindow.ROWS, MyWindow.COLUMNS)

    def button_first_click(self, button):
        self.get_mines(button.number, self.buttons, MyWindow.COUNT_MINES,
                       MyWindow.ROWS, MyWindow.COLUMNS)
        self.count_mines_around()
        self.print_buttons_on_console()
        MyWindow.IS_FIRST_CLICK = False

    def count_mines_around(self):
        for i in range(1, MyWindow.ROWS + 1):
            for j in range(1, MyWindow.COLUMNS + 1):
                btn = self.buttons[i][j]
                if not btn.IS_MINE:
                    count_mines = self.select_neighbours_for_ceil(i, j)
                    btn.count_mines = count_mines

    def bypass_in_width(self, x, y, q):
        for dx in MyWindow.POSSIBLE_COORDINATE_CHOICE:
            for dy in MyWindow.POSSIBLE_COORDINATE_CHOICE:
                next_button = self.buttons[x + dx][y + dy]
                if not next_button.is_open and 1 <= next_button.x <= MyWindow.ROWS and \
                        1 <= next_button.y <= MyWindow.COLUMNS and next_button not in q:
                    q.append(next_button)

    def select_neighbours_for_ceil(self, i: int, j: int, count_mines=0):
        for row_dx in MyWindow.POSSIBLE_COORDINATE_CHOICE:
            for col_dx in MyWindow.POSSIBLE_COORDINATE_CHOICE:
                neighbour = self.buttons[i + row_dx][j + col_dx]
                if neighbour.IS_MINE:
                    count_mines += 1
        return count_mines

    def breadth_first_search(self, button):
        queue = [button]
        while queue:
            current_button = queue.pop()
            if current_button.count_mines:
                self.get_colors_by_count_mines(current_button)
            else:
                current_button.config(text='')
            self.get_button_config(current_button)
            if not current_button.count_mines:
                x, y = current_button.x, current_button.y
                self.bypass_in_width(x, y, queue)

    def print_buttons_on_console(self):
        for i in range(1, MyWindow.ROWS + 1):
            for j in range(1, MyWindow.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.IS_MINE:
                    print('B', end=' ')
                else:
                    print(btn.count_mines, end=' ')
            print()

    @staticmethod
    def start():
        GridButtons().grid_buttons()
        MyWindow.win.mainloop()


class Menu(MyWindow):

    def create_menubar(self):
        menubar = tk.Menu(self.win)
        self.grid_menu(menubar)
        self.settings_menu(menubar)

    def grid_menu(self, menu):
        self.win.config(menu=menu)

    def settings_menu(self, menu):
        settings_menu = tk.Menu(menu, tearoff=0)
        labels = ("Нова гра", "Налаштування", "Вихід")
        settings_menu.add_command(label=labels[0], command=MenuCommands().reload)
        settings_menu.add_command(label=labels[1], command=MenuCommands().create_settings_window)
        settings_menu.add_command(label=labels[2], command=self.win.destroy)

        menu.add_cascade(label="Файл", menu=settings_menu)


class GridButtons(MyWindow):
    def grid_buttons(self):
        Menu().create_menubar()
        count = 1
        for i in range(1, MyWindow.ROWS + 1):
            for j in range(1, MyWindow.COLUMNS + 1):
                button = self.buttons[i][j]
                button.number = count
                button.grid(row=i, column=j, stick='NWES')
                count += 1
        self.grid_freeze_buttons_rows()
        self.grid_freeze_buttons_columns()

    def grid_freeze_buttons_rows(self):
        for i in range(1, MyWindow.ROWS + 1):
            tk.Grid.rowconfigure(self.win, i, weight=1)

    def grid_freeze_buttons_columns(self):
        for i in range(1, MyWindow.COLUMNS + 1):
            tk.Grid.columnconfigure(self.win, i, weight=1)


class MenuCommands(Menu):

    def create_settings_window(self):
        windows_settings = tk.Toplevel(self.win)
        windows_settings.wm_title("Налаштування")
        self.grid_entries(windows_settings)

    def grid_entries(self, win_settings: callable):
        titles_for_labels = ("Кількість рядків:", "Кількість стовпчиків:", "Кількість мін:")
        values_for_insert = (MyWindow.ROWS, MyWindow.COLUMNS, MyWindow.COUNT_MINES)
        keys_to_dict = ('row', 'column', 'mines')
        entries_dict = {}
        for i in range(3):
            entry = tk.Entry(win_settings)
            entry.insert(0, values_for_insert[i])
            entry.grid(row=i, column=1, padx=20, pady=20)
            tk.Label(win_settings, text=titles_for_labels[i]).grid(row=i, column=0)
            entries_dict[keys_to_dict[i]] = entry
        button = self.create_buttons(win_settings, 'Застосувати',
                                     command=lambda: self.change_settings(**entries_dict))
        button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row, column, mines):
        try:
            list(map(int, (row.get(), column.get(), mines.get())))
        except ValueError:
            showerror("Помилка!", "Введене значення повинне бути числом")
            return
        MyWindow.ROWS = int(row.get())
        MyWindow.COLUMNS = int(column.get())
        MyWindow.COUNT_MINES = int(mines.get())
        max_count_mines = (MyWindow.ROWS * MyWindow.COLUMNS) - 5
        self.check_count_mines(MyWindow.COUNT_MINES, max_count_mines)
        self.check_input_values(MyWindow.ROWS, MyWindow.COLUMNS)
        self.reload()

    @staticmethod
    def check_count_mines(count: int, value: int):
        if isinstance(count, int) and isinstance(value, int):
            if count > value:
                return showerror('Помилка!', "Введена надто велика кількість мін")

    @staticmethod
    def check_input_values(rows: int, columns: int):
        check_value_less_60 = rows > 60 or columns > 60
        check_value_more_5 = rows < 5 or columns < 5
        if check_value_less_60 or check_value_more_5:
            return showerror('Помилка!', 'Надто велике або надто мале значення рядків і '
                                         'стовпчиків,значення повинне бути в діапазоні 5 - 60')

    def reload(self):
        [child.destroy() for child in self.win.winfo_children()]
        super().__init__()
        GridButtons().grid_buttons()
        MyWindow.IS_FIRST_CLICK = True
        MyWindow.IS_GAME_OVER = False


a = MyWindow()
a.start()
