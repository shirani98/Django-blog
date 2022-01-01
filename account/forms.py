from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.forms import models, widgets
from ckeditor.widgets import CKEditorWidget
from post.models import Category, Post
from .models import CustomUser
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    password = forms.CharField( max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))
                                                           
    
class UserCreate(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'})) 
    phone = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))
    confirmed_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))
                                                                                          
 
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmed_password = cleaned_data.get("confirmed_password")
        if password != confirmed_password:
            raise forms.ValidationError("password must match")
            
class AddPostForm(forms.Form):
    
    choise_status =(("d","Draft"),("p","Publish"))
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text','placeholder': 'Enter ...'}))
    slug = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text','placeholder': 'Enter ...'}))
    body = forms.CharField(widget=CKEditorWidget(attrs={"rows":"5", "class":"form-control",'placeholder': 'Enter ...'}))
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control','id' : 'exampleInputFile', 'type': 'file'}))
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    status = forms.ChoiceField(choices=choise_status,widget=forms.Select(attrs={'class': 'form-control'}))
    
    
class UpdateForm(forms.ModelForm):
    choise_status =(("d","Draft"),("p","Publish"))
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text','placeholder': 'Enter ...'}))
    slug = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text','placeholder': 'Enter ...'}))
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5", "class":"form-control",'placeholder': 'Enter ...'}))
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control','id' : 'exampleInputFile', 'type': 'file'}))
    status = forms.ChoiceField(choices=choise_status,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title','slug','body','image','category','status']