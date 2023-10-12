'''
this function is used to extract
Authorization header section and separate
this "Token [token]" to "Token" and "[token]"
'''


def get_token(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Now you can access the Authorization header value
    if authorization_header:
        _, token = authorization_header.split(' ')
        return token