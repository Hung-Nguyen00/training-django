from core.exceptions import GenericException


class ProductDoesNotExistException(GenericException):
    code = 5000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The product does not exist."
        super().__init__(message=message)


class QuantityOfProductExceedException(GenericException):
    code = 5000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Your purchase quantity exceeds the existing."
        super().__init__(message=message)
        
        
class ThereAreNotAnyProductToOrderException(GenericException):
    code = 5001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "There are not any products to order."
        super().__init__(message=message)