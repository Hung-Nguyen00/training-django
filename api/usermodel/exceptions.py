from core.exceptions import GenericException


class UserNotExistsException(GenericException):
    code = 2016
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User does not exist"
        super().__init__(message=message)