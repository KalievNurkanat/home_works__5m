import random
from rest_framework.generics import CreateAPIView
from users.serializers import CodeRedisSerilizer
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

def generate_confirmation_code(user_id: int, code:str):
    key = f"Confirmation_code:{user_id}"
    cache.set(key, code, timeout=300)


def confirm_code(user_id:int, code:str):
    key = f"Confirmation_code:{user_id}"
    saved_code = cache.get(key)

    if not saved_code:
        return False
    
    if saved_code != code:
        return False
    
    cache.delete(key)
    return True

class GenerateConfirmaitonCode(CreateAPIView):
    def post(self, request):
        user = request.user

        code = str(random.randint(100000, 999999))
        if not user.is_authenticated:
            raise ValidationError("u need to authorize")
        
        generate_confirmation_code(user.id, code) 
           

        return Response(data={"Code saved. Check the Redis"}, status=200)
    
class CheckConfirmationCode(CreateAPIView):
    serializer_class = CodeRedisSerilizer
    def post(self, request):
        user = request.user
        code = request.data.get('code')


        if confirm_code(user.id, code):
            return Response(data="Code comfirmed and deleted from cache", status=200)
        
        return Response(data="Either code is incorrect or expired", status=400)




    

