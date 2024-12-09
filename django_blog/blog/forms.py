from django import forms
from .models import Post, CustomUser
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
    model = Post
    fields = "__all__"