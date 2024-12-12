from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, CustomUserCreationForm, PostForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

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
    

#POST CRUD
class PostListView(ListView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    #comment feature
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post-detail',pk=self.object.pk)
        return self.get(request,*args,**kwargs)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = 'blog/post_form.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    #ensure only author can perform task
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

    #author to current user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = 'blog/post_form.html'

class PostDeleteView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('posts')
    template_name = 'blog/post_confirm_delete.html'

    #ensure only author can perform task
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#Commenting

class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.object.post.pk})
    
    #ensure only author can perform task
    def test_func(self):
        return self.request.user == self.get_object().author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.object.post.pk})
    
    #ensure only author can perform task
    def test_func(self):
        return self.request.user == self.get_object().author
    

class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.kwargs['pk']})
    

    #search
def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query) | Q(content__icontains=query)).distinct()
    return render(request,'blog/search_results.html',{'posts':posts})

#tagging
class PostByTagView(ListView):
    model = Post
    template_name = 'blog/post_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug'])