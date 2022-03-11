import django.contrib.auth.password_validation as password_validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_core
from rest_framework.serializers import ValidationError as DRFValidationError

class EmailValidator(object):
    def __call__(self, email):
        if email.strip() == "":
            raise DRFValidationError("Email is required.", code=2000)

        try:
            validate_email_core(email)
        except ValidationError as error:
            raise DRFValidationError(error.messages[0], code=2007)

        # if User.objects.filter(email__iexact=email.lower()).exists():
        #     raise DRFValidationError("A user is already registered with this e-mail address.", code=2004)


class PasswordValidator(object):
    def __init__(self, old_password=None):
        self.old_password = old_password

    def __call__(self, password):
        try:
            password_validators.validate_password(password)
        except ValidationError as error:
            raise DRFValidationError(error.messages[0], code=2006)

        if self.old_password and self.old_password == password:
            raise DRFValidationError("Old password and new password can not be the same", code=2010)


