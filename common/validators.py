import datetime
from rest_framework.exceptions import ValidationError

def validate_age(token):
    birthday_str = token.get("birthday")

    if not birthday_str:
        raise ValidationError("Введите дату рождения")

    birthday = datetime.date.fromisoformat(birthday_str)
    today = datetime.date.today()

    age = today.year - birthday.year - (
        (today.month, today.day) < (birthday.month, birthday.day)
    )

    if age < 18:
        raise ValidationError("Вам должно быть 18, чтобы создать продукт")