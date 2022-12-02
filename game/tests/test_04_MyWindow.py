from ..game import MyWindow


class TestMyWindowInit:

    def test_valid_length_list(self):
        my_wnd = MyWindow()
        assert len(my_wnd.buttons) == 12
