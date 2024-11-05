from django.db import models

# Create your models here.

'''
Create a Book class with the following fields:
title: CharField with a maximum length of 200 characters.
author: CharField with a maximum length of 100 characters.
publication_year: IntegerField.

'''
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

def __str__(self):
    return self.title