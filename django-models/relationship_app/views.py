from django.shortcuts import render
from .models import Book, Library
from django.views.generic.detail import DetailView

# Create your views here.

#all books
def books(request):
    book_list = Book.objects.all()
    data = {"books":book_list}
    return render(request,'list_books.html',data)

class LibrairyDetails(DetailView):
    model = Library
    template_name = 'library_details.html'
    context_object_name = 'library'
