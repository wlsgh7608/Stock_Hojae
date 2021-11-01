import jwt
import json


from hojae.settings import SECRET_KEY
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginConfirm:
    def __init__(self,og_function):
        self.og_function= og_function

    def __call__(self,request,*args,**kwargs):
        token = request.headers.get("Authorization",None)
        token = token[4:] # jwt 토큰만 가져오기
        try:
            if token:
                token_payload = jwt.decode(jwt = token,key =SECRET_KEY,algorithms='HS256')
                user = User.objects.get(username = token_payload['username'])
                print("user is ", token_payload)
                request.user = user
                return self.og_function(self,request,*args,**kwargs)
            return JsonResponse({'message':"로그인이 필요합니다."},status = 401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':"토큰이 만료되었습니다."},status = 401)
        except jwt.DecodeError:
            return JsonResponse({'message':"유효하지 않은 유저입니다."},status = 401)
        except User.DoesNotExist:
            return JsonResponse({'message':"유저가 존재하지 않습니다.."},status = 401)
        