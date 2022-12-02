import tkinter as tk

import pytest

from ..buttons import MyButton


@pytest.fixture
def create_button():
    win = tk.Tk()
    button = MyButton(win, x=1, y=1)
    return button
