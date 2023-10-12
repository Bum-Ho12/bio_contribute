'''
this function checks the existence
of tokens and returns True or False.
It is used to validate the token shared
in header part of the request.
mimics IsAuthenticated permission_class
but overrides the settings.USER_MODEL.
'''

from .tokenizer import AuthToken
from .token_getter import get_token

def is_authenticated(request):
    token = get_token(request)
    try:
        AuthToken.objects.get(key= token)
        return True
    except:
        return False