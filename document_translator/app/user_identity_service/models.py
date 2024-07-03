import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class DepartmentLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    created_by = models.UUIDField(null=False)
    created_by_datetime = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_datetime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'department_lkp'

    def __str__(self):
        return self.name

    
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    email = models.CharField(max_length=100, null=False, unique=True)
    role_id = models.ForeignKey('RoleLkp', on_delete=models.PROTECT,
                                    null=True, db_column='role_id')
    department_lkp_id = models.ForeignKey('DepartmentLkp', on_delete=models.PROTECT,null=True, db_column='department_lkp_id')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('self', related_name='created_users', null=True,
                                   on_delete=models.PROTECT, db_column='created_by')
    created_by_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey('self', related_name='updated_users', 
                                   on_delete=models.PROTECT, null=True, db_column='updated_by')
    updated_by_date = models.DateTimeField(auto_now=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name

class RoleLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name='created_roles', null=False,
                                   on_delete=models.PROTECT, db_column='created_by')
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.ForeignKey(User, related_name='updated_roles', 
                                   on_delete=models.PROTECT, null=True, db_column='updated_by')
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'role_lkp'

    def __str__(self):
        return self.role