import tkinter as tk
from abc import abstractmethod

from .mixins import MinesMixin


class MyButton(tk.Button, MinesMixin):

    def __init__(self, master, x: int, y: int, number: int = 0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Arial 15', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.IS_MINE = False
        self.count_mines = 0
        self.is_open = False
        self.buttons = []

    def click_button(self, clicked_button, game_over: bool, first_click: bool):
        if game_over:
            return
        if first_click:
            self.button_first_click(clicked_button)
        if clicked_button.IS_MINE:
            self.button_is_mine(clicked_button)
        else:
            if clicked_button.count_mines:
                self.get_colors_by_count_mines(clicked_button)
            else:
                self.breadth_first_search(clicked_button)
        self.get_button_config(clicked_button)

    @staticmethod
    def create_buttons(window: callable, text: str, command: callable):
        return tk.Button(window, text=text, command=command)

    @staticmethod
    def get_button_config(button, state: str = 'disabled', relief: callable = tk.SUNKEN):
        button.is_open = True
        button.config(state=state)
        button.config(relief=relief)

    @abstractmethod
    def button_first_click(self, clicked_button):
        pass

    @abstractmethod
    def breadth_first_search(self, clicked_button):
        pass

    @abstractmethod
    def button_is_mine(self, button):
        pass

    def __repr__(self):
        return f'Button {self.x} {self.y} {self.IS_MINE} {self.number}'


