from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Book, Library
from .forms import RegistrationForm
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


#registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user) #log th user in after registration
            return redirect('book-list')
    else:
        form = RegistrationForm()
        return render(request,'register.html',{'form':form})
    

#login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('book-list')
            else:
                messages.error(request,'Invalid username or password!')
    else:
        form = AuthenticationForm()
        return render('request','login.html',{'form':form})
    

#logout
def logout(request):
    logout(request)
    return redirect(login)