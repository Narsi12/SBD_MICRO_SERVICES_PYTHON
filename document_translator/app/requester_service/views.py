import logging
from document_translator.global_views import MixinClass
from rest_framework import viewsets
from .models import LanguageLkp
from .serializers import LanguageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .authentication import UserAuthentication

logger = logging.getLogger(__name__)

class Pagination(PageNumberPagination):
    page_size = 10

class LanguageImplementation(MixinClass,viewsets.ModelViewSet):
    authentication_classes = (UserAuthentication,)
    serializer_class = LanguageSerializer
    pagination_class = Pagination
    queryset = LanguageLkp.objects.all()
    model = LanguageLkp

    def addLanguage(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def getLanguage(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def updateLanguageByHashId(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)
    
    def getLanguageByHashId(self,request,*args,**kwargs):
        return self.getById(request,*args,**kwargs)    

    def deleteLanguageByHashId(self, request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)