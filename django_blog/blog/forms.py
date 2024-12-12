from django import forms
from .models import Post, CustomUser, Comment
from django.contrib.auth.forms import UserCreationForm


#custom registration form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already taken')
            return email
        
#Profile management 
class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email','bio']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user','None')
        super().__init__(*args,**kwargs)

    def save(self,commit=True):
        post = super().save(commit=False)
        if self.user:
            post.author = self.user
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
