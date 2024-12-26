from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

from django.core import validators

from django.db import models

from datetime import datetime

from permissiongroupdefines.models import PermissionGroupDefine

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, first_name, last_name, father_name, gender, date_of_birth,
                     national_code, recruitment_date, is_superuser, is_staff, is_active):

        user = self.model(phone_number=phone_number, password=password, first_name=first_name, last_name=last_name,
                          father_name=father_name, gender=gender, date_of_birth=date_of_birth,
                          national_code=national_code, recruitment_date=recruitment_date, is_superuser=is_superuser,
                          is_staff=is_staff, is_active=is_active, record_date=datetime.now())

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, first_name, last_name, father_name, gender, date_of_birth,
                    national_code, recruitment_date, is_superuser, is_staff, is_active):
        return self._create_user(phone_number, password, first_name, last_name, father_name, gender, date_of_birth,
                                 national_code, recruitment_date, is_superuser, is_staff, is_active)

    def create_superuser(self, phone_number, password, first_name, last_name, father_name, gender, date_of_birth,
                         national_code, recruitment_date):
        return self._create_user(phone_number, password, first_name, last_name, father_name, gender, date_of_birth,
                                 national_code, recruitment_date, True, True, True)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, validators=[validators.RegexValidator(
        regex=r'^989[0-3,9]\d{8}$', message="Phone number must be entered in the format: '989-3-9'."
    )])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')))
    role = models.ForeignKey('roles.Role', blank=True, null=True, on_delete=models.RESTRICT, default=None)
    permission_group = models.ForeignKey('permissiongroups.PermissionGroup', blank=True, null=True,
                                         on_delete=models.RESTRICT, default=None)
    date_of_birth = models.DateField()
    national_code = models.CharField(max_length=10, unique=True)
    recruitment_date = models.DateField()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    record_date = models.DateField()
    recorder = models.ForeignKey('self', blank=True, null=True, on_delete=models.RESTRICT, default=None)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'father_name', 'gender', 'date_of_birth', 'national_code',
                       'recruitment_date']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'users'

    @property
    def permissions_list(self) -> list[str]:
        if pgd := PermissionGroupDefine.objects.filter(permission_group=self.permission_group).all():
            return [p.permission.name for p in pgd]


class LoginLog(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.RESTRICT, null=False)
    login_date = models.DateTimeField()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        db_table = 'login_logs'