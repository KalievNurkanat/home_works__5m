import datetime
from rest_framework.exceptions import ValidationError

def validate_age(user):
    if not user.birthday:
        raise ValidationError("Укажите дату рождения")
    
    birthday = user.birthday
    today = datetime.date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    
    if age < 18:
        raise ValidationError("Вам должно быть 18, чтобы создать продукт") 
    