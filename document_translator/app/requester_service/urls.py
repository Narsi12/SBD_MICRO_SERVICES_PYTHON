from django.contrib import admin
from django.urls import path, include
from .views import LanguageImplementation

urlpatterns = [ 
    path('languages', LanguageImplementation.as_view(
        {'post': 'addLanguage', 'get': 'getLanguage'}), name='Language'),
    path('languages/<uuid:pk>', LanguageImplementation.as_view(
        {'put': 'updateLanguageByHashId', 'delete': 'deleteLanguageByHashId',
         'get': 'getLanguageByHashId'}), name='Language_detail'),
]