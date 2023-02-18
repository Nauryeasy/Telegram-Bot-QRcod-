from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    URL_STATE = ListItem()
    QR_STATE = ListItem()


if __name__ == '__main__':
    print(TestStates.all())