class UserNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserAlreadyExistsException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
