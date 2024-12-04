from django.shortcuts import redirect, render
from .models import Post
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'blog/register.html',{'form':form})