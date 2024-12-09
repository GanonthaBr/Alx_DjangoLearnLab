from django.shortcuts import redirect, render
from .models import Post
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
        return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'blog/register.html',{'form':form})

#Profile

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('profile')
    else:
        form  = ProfileForm(instance=user)
        return render(request,'blog/profile.html',{'form':form})