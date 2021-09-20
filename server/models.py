from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify

class UserManager(BaseUserManager):

  def create_user(self, email, password):
    if not email:
      raise ValueError('Users must have email')
    if not password:
      raise ValueError('Every user must have a password')

    user = self.model(
      email=self.normalize_email(email)
    )

    user.set_password(password)

    user.save(using=self._db)

    return user

  def create_superuser(self, email, password):
    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
    )

    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)


class User(AbstractBaseUser):
  email = models.EmailField(max_length=100, unique=True)
  password = models.CharField(max_length=200)
  date_created = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'

  REQUIRED_FIELDS = ('password',)

  objects = UserManager()

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True


class UserNote(models.Model):
  title = models.CharField(max_length=200)
  note = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  slug = models.SlugField(null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    title_contents = self.title.lower().split(' ')
    self.slug = '_'.join(title_contents)
    super(UserNote, self).save()
  