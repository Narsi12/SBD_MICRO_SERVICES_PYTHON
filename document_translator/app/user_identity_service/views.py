import logging
from .models import User, RoleLkp
from rest_framework.views import APIView
from .authentication import UserAuthentication
from django.contrib.auth import authenticate
from document_translator.enums import ErrorCode
from document_translator.global_views import MixinClass
from document_translator.middleware import CustomAPIException
from rest_framework import generics, status, viewsets
from document_translator.responses import SuccessResponse
from .serializers import UserSerializer, LoginSerializer, RoleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

class Pagination(PageNumberPagination):
    page_size = 10

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User registered in successfully.")
        result = SuccessResponse(code = status.HTTP_201_CREATED, status="CREATED",message='User Registered Successfully')
        return result.http_response(status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            logger.error("Email or password not provided.")
            raise CustomAPIException(code = ErrorCode.INVALID_INPUT, detail="Email and password are required fields.")
        user = authenticate(email=email, password=password)
        if not user:
            logger.error("Invalid email or password.")
            raise CustomAPIException(code = ErrorCode.UNAUTHORIZED)
        query_user = User.objects.get(email = email)
        if query_user.is_active:
            refresh = RefreshToken.for_user(user)
            tokens = {'refresh': str(refresh),'access': str(refresh.access_token)}
            logger.info(f"User with email Id - {email} logged in successfully.")
            result=SuccessResponse(code=status.HTTP_201_CREATED,status='CREATED',message='Token generated successfully',data=tokens)
            return result.http_response(status=201)

class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        result = SuccessResponse(code = status.HTTP_200_OK, status = 'OK', message = 'User Logged out successfully.')
        return result.http_response(status=status.HTTP_200_OK)

class UserImplementation(MixinClass,viewsets.ModelViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = Pagination
    queryset = User.objects.all()
    model = User

    def getUser(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def getUserByUUId(self,request,*args,**kwargs):
        return self.getById(request,*args,**kwargs)  

    def updateUserByUUId(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)

    def deleteUserByUUId(self, request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)
    
class UserEmailImplementation(APIView):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        email = request.query_params.get('email')
        if email:
            user = User.objects.get(email=email)
            serializer = self.serializer_class(user)
            result = SuccessResponse(code = status.HTTP_200_OK, status = 'OK', message = 'User Logged out successfully.',data = serializer.data)
            return result.http_response(status=status.HTTP_200_OK)
            
class RoleImplementation(MixinClass,viewsets.ModelViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    pagination_class = Pagination
    queryset = RoleLkp.objects.all()
    model = RoleLkp

    def addRole(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def getAllRoles(self,request,*args,**kwargs):
        return self.list(request, *args, **kwargs)
    
    def getRoleByUUId(self,request,*args,**kwargs):
        return self.getById(request,*args,**kwargs)  
    
    def updateRoleByUUId(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def deleteRoleByUUId(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)       