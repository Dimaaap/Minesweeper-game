from random import randint

import pytest


from game import MyButton, MyWindow


@pytest.fixture
def create_button():
    button = MyButton(MyWindow.win, x=1, y=1)
    button.count_mines = randint(0, 7)
    button.config(text=button.count_mines)
    return button['text']


@pytest.fixture
def button_is_mine():
    button = MyButton(MyWindow.win, x=1, y=1)
    button.is_mine = True
    return button


@pytest.fixture
def is_game_over():
    MyWindow.IS_GAME_OVER = True
    return MyWindow.IS_GAME_OVER

