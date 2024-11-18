from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    profile_photo = models.ImageField()
    data_of_birth = models.DateField()


class Author(models.Model):
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