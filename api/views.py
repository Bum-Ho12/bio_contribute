import datetime
from .tokenizer import AuthToken # class that is used to generate Tokens
from rest_framework import status
from .token_getter import get_token
from .models import Account, Specimen
from .auth_validity import is_authenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from .serializers import AccountSerializer,SpecimenSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes,parser_classes

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def all_specimen(request):
    if request.method=='GET':
        specimens   = Specimen.objects.all()
        serializer  = SpecimenSerializer(specimens,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def register_account(request):
    if request.method == 'POST':
        serialized              = AccountSerializer(data=request.data)
        username                = request.data.get('username')
        first_name, last_name   = username.split(' ') if ' ' in username else(username, '')
        data                    = {}
        if serialized.is_valid():
            account             = serialized.save()
            AuthToken.objects.create(user=account)
            obj                 = Account.objects.get(email_address = account.email_address)
            obj.token           = AuthToken.objects.get(user=obj).key
            obj.first_name,obj.last_name = first_name,last_name
            obj.save()
            sr                  = AccountSerializer(obj)
            data = sr.data
            username            = obj.first_name + ' ' + obj.last_name
            data['username']    = username
            return Response(data= data,status=status.HTTP_201_CREATED)
        else:
            data                = serialized.errors
            return Response(data, status=status.HTTP_501_NOT_IMPLEMENTED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def login_account(request):
    try:
        email                   = request.data['email_address']
        password                = request.data['password']
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        user                    = Account.objects.get(email_address = email,password = password)
        try:
            user_token          = AuthToken.objects.get(user=user).key
        except:
            user_token          = AuthToken.objects.create(user=user)
            user.token          = user_token.key
            user.save()
        data                    = {}
        data['token']           = user.token
        data['email_address']   = user.email_address
        data['username']        = user.first_name + ' '+ user.last_name
        data['phone_number']    = user.phone_number
        return Response(data=data,status=status.HTTP_202_ACCEPTED)
    except:
        data = {}
        data['error'] = 'Please register to gain access!'
        return Response(data=data,status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    try:
        account         = Account.objects.get(token = get_token(request))
    except:
        response = {'error': 'Unable to get user!'}
        return Response(data= response,status=status.HTTP_401_UNAUTHORIZED)
    sr = AccountSerializer(account)
    data = sr.data
    data['username'] = account.first_name + ' ' + account.last_name
    return Response(data= data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser,FormParser])
def update_account(request):
    if is_authenticated(request):
        try:
            account         = Account.objects.get(token=get_token(request))
        except:
            data            = {}
            data['error']   = 'account does not exist'
            return Response(data=data,status=status.HTTP_404_NOT_FOUND)
        serialized          = AccountSerializer(account,data=request.data,partial=True)
        if serialized.is_valid():
            acc            = serialized.save()
            user           = Account.objects.get(email_address = acc.email_address)
            try:
                user_token          = AuthToken.objects.get(user=user).key
            except:
                user_token          = AuthToken.objects.create(user=user)
                user.token          = user_token.key
                user.save()
            data                    = {'token':user_token}
            data['email_address']   = user.email_address
            data['first_name']      = user.first_name
            data['last_name']       = user.last_name
            data['phone_number']    = user.phone_number
            return Response(data=data,status=status.HTTP_200_OK)
    else:
        data = {'error':'invalid token provided!'}
        return Response(data=data,status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_account(request):
    try:
        account             = Account.objects.get(token = get_token(request))
    except:
        response            = {}
        response['error']   = 'wrong credentials'
        return Response(data=response,status=status.HTTP_401_UNAUTHORIZED)
    token                   = AuthToken.objects.get(user=account)
    token.delete()
    data                    = {}
    data['success']         = 'Signed out'
    return Response(
        data =data,status= status.HTTP_200_OK
    )


@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def create_specimen(request):
    if is_authenticated(request):
        sp_sr               = SpecimenSerializer(data = request.data)
        files               = request.FILES.get('image')
        if files:
            request.data.pop('image')
            if sp_sr.is_valid():
                author      =Account.objects.get(token=get_token(request))
                sp_sr.save(author = author)
                obj         = Specimen.objects.get(id = sp_sr.data['id'])
                context     = sp_sr.data
                obj.image   = files
                obj.save()
                context['image'] = obj.image.url
                return Response(data = context, status=status.HTTP_201_CREATED)
        else:
            data            = {}
            data['error']   = 'Image not captured!'
            return Response(data=data,status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        data                ={}
        data['error']       = 'Not authenticated or invalid user!'
        return Response(data = data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
@permission_classes([AllowAny])
@parser_classes([FormParser,MultiPartParser,JSONParser])
def update_specimen(request):
    if is_authenticated(request):
        try:
            sp         = Specimen.objects.get(id=request.data.get('id'))
            files               = request.FILES.get('image')
        except:
            data            = {}
            data['error']   = 'object does not exist'
            return Response(data=data,status=status.HTTP_404_NOT_FOUND)
        sp_sr = SpecimenSerializer(sp,data=request.data,partial = True)
        if files:
            request.data.pop('image')
            if sp_sr.is_valid():
                sp_sr.save()
                obj         = Specimen.objects.get(id = sp_sr.data['id'])
                context     = sp_sr.data
                obj.image   = files
                obj.save()
                context['image'] = obj.image.url
                return Response(data = context, status=status.HTTP_201_CREATED)
            else:
                data = {'error': 'error updating object'}
                return Response(data=data, status=status.HTTP_409_CONFLICT)
        else:
            if sp_sr.is_valid():
                sp_sr.save()
                context = sp_sr.data
                return Response(data=context,status=status.HTTP_200_OK)
            else:
                data = {'error': 'error updating object'}
                return Response(data=data, status=status.HTTP_409_CONFLICT)
    else:
        data = {'error':'invalid token used'}
        return Response(data=data,status= status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def delete_specimen(request):
    if is_authenticated(request):
        specimen    = Specimen.objects.get(id = request.data.get('id'))
        specimen.delete()
        data = {'success': 'specimen deleted successfully!'}
        return Response(data=data,status=status.HTTP_200_OK)
    data = {'error':'invalid token provided!'}
    return Response(data=data,status=status.HTTP_401_UNAUTHORIZED)

