from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, profile_photo, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, profile_photo=profile_photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, profile_photo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, date_of_birth, profile_photo, password, **extra_fields)

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photo/')
    data_of_birth = models.DateField()
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book","can add book"),
            ("can_change_book",'can change book'),
            ("can_delete_book",'can delete book'),
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    list_choices = ['Admin','Librarian','Member']
    user = models.OneToOneField(User)
    role = models.CharField(choices=list_choices)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


#signal for authmatic UserProfile creation when new user is registered
@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()