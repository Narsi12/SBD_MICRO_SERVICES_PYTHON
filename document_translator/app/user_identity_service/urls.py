from django.urls import path
from .views import (RegisterView, LoginView, UserImplementation, UserEmailImplementation, LogoutAPIView,
                    RoleImplementation)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('users', UserImplementation.as_view(
        {'get': 'getUser'}), name='user_list'),
    path('user/<uuid:pk>', UserImplementation.as_view(
        {'put': 'updateUserByUUId', 'delete': 'deleteUserByUUId',
         'get': 'getUserByUUId'}), name='user_detail'),
    path('user_email', UserEmailImplementation.as_view(), name='user_email'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('role', RoleImplementation.as_view(
        {'post': 'addRole', 'get': 'getAllRoles'}), name='Role'),
    path('role/<uuid:pk>', RoleImplementation.as_view(
        {'put': 'updateRoleByUUId', 'delete': 'deleteRoleByUUId',
            'get': 'getRoleByUUId'}), name='Role_detail'),
]