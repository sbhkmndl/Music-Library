from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

from .send_mail import send_rest_password_email
from .code import code_generator

USERNAME_VALIDATE = '^[a-zA-Z0-9._]*$'


# User authentication model
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                validators=[RegexValidator(
                                    regex=USERNAME_VALIDATE,
                                    message='username contain only "._"',
                                    code='invalid username'
                                )])
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True


# User details model

def upload_image_location(instance, filename):
    return "%s/img/%s" % (instance.id, filename)


class UserDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_set')
    name = models.CharField(max_length=200, blank=True)
    user_image = models.ImageField(upload_to=upload_image_location,
                                   null=True, blank=True,
                                   height_field='height_field',
                                   width_field='height_field', default=None)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# if no name provide add username as name
def pre_save_add_name(sender, instance, *args, **kargs):
    if not instance.name:
        instance.name = instance.user.username


pre_save.connect(pre_save_add_name, sender=UserDetail)


# create UserDetails model after create User model
def post_save_create_user_details(sender, instance, created, *args, **kargs):
    if created:
        try:
            UserDetail.objects.create(user=instance)
        except Exception as e:
            print(e.args)  # arguments stored in .args
            pass


post_save.connect(post_save_create_user_details, sender=settings.AUTH_USER_MODEL)


# forget password model
class PasswordForget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


def pre_save_add_code(sender, instance, *args, **kargs):
    if not instance.code:
        temp_code = get_code()
        instance.code = temp_code
        send_rest_password_email(temp_code, instance.user.email)


def get_code():
    code = code_generator()
    if PasswordForget.objects.filter(Q(code=code), Q(active=True)).exists():
        code_generator()
    return code


pre_save.connect(pre_save_add_code, sender=PasswordForget)