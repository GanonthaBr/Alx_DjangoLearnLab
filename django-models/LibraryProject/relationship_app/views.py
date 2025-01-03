from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Library
from .models import Book
from .forms import RegistrationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.decorators import permission_required
from django.views import View

# Create your views here.

#all books
def list_books(request):
    book_list = Book.objects.all()
    data = {"books":book_list}
    return render(request,'relationship_app/list_books.html',data)

@permission_required('relationship_app.can_add_book',raise_exception=True)
def add_book_view(request):
    if request.method == 'POST':
        return HttpResponse('Added new book')
    

@permission_required('relationship_app.can_change_book',raise_exception=True)
def update_book_view(request,pk):
    book = get_list_or_404(Book,pk=pk)
    if request.method == 'PUT':
        return HttpResponse('Updated book')
    
    
@permission_required('relationship_app.can_delete_book',raise_exception=True)
def delete_book_view(request,pk):
    if request.method == 'DELETE':
        book = get_list_or_404(Book,pk=pk)
        book.delte()
        return HttpResponse('Book deleted!')





class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


#registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserCreationForm()
            login(request,user) #log th user in after registration
            return redirect('book-list')
    else:
        form = RegistrationForm()
        return render(request,'relationship_app/register.html',{'form':form})
    

#login

class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'relationship_app/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book-list')
            else:
                messages.error(request, 'Invalid username or password!')
        return render(request, self.template_name, {'form': form})

#logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


# Role checking functions

# def is_admin(user):
#     return user.userprofile.role == 'Admin'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

# View controlled access



def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')
# @login_required
# @user_passes_test(is_admin)
# def admin_view(request):
#     return HttpResponse('This is the admin view')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return HttpResponse('This is the member view')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse('This is the librarian view')