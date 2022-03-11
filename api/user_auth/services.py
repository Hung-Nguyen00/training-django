
from usermodel.models import User
from usermodel.exceptions import UserNotExistsException

def get_user(user_id: str) -> User:
    try:
        return User.objects.get(pk=user_id)
    except Exception:
        raise UserNotExistsException()

