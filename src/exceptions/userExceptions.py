class UserNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserAlreadyExistsException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidPayloadException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidPasswordException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DatabaseException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
