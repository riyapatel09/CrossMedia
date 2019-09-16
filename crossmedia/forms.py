from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Post
from django.shortcuts import render_to_response
#from django.contrib.formtools.wizard.views import SessionWizardView


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
   # image = forms.ImageField()
   # birth_date = forms.DateField()

    class Meta:
        model = User
        #fields elow are to be distplayed on the form
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender']

class RegisterFormStepOne(forms.Form):
    user_birthdate = forms.DateField(required=True)

class RegisterFormStepTwo(forms.Form):
    parent_email = forms.EmailField(required=True, help_text='Enter Your Parents User Email of Crossmedia')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content']