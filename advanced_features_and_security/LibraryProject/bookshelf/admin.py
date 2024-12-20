from django.contrib import admin
from .models import Book, CustomUser, Author, CustomUserAdmin


# Register your models here.

admin.site.register(Book)
admin.site.register(CustomUser, CustomUserAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ['publication_year']
    search_fields = ['title', 'author']