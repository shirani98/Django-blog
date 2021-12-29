from django.contrib import messages
from django.core.checks.messages import Info
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from account.authenticate import EmailPhoneBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from account.forms import AddPostForm, LoginForm, UpdateForm, UserCreate
from account.models import CustomUser
from post.models import Category, Post
from django.views.generic.edit import UpdateView


# Create your views here.

def loginfun(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('account:dash')
            else:
                messages.error(request, 'wrong username or password', 'warning')
                
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register_user(request):
    if request.method == "POST":
        form = UserCreate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            emailfound = data["email"]
            phonefound = data["phone"]
            if CustomUser.objects.filter(phone=phonefound).exists():
                messages.error(request,"'This phone already exists'")
                return render (request,"account/signup.html",{"form":form})
            if CustomUser.objects.filter(email=emailfound).exists():
                messages.error(request,"'This email already exists'")
                return render (request,"account/signup.html",{"form":form})
            CustomUser.objects.create_user(data["email"],data["name"],data["password"])
            return redirect("account:login")
    form = UserCreate()
    return render (request,"account/signup.html",{"form":form})

@login_required
def showdashboard(request):
    if request.user.is_superuser :
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(writer = request.user)
    
    context = {
        "posts" : posts
    }
    return render(request,"account/dash/dash.html",context)
@login_required
def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data["title"]
            slug = data["slug"]
            body= data["body"]
            image = data["image"]
            category_field = data["category"]
            if request.user.is_superuser or request.user.is_owner:
                status = data["status"]
            else:
                status = "d"
            writer = request.user
            post = Post(title = title,slug = slug,body = body,writer = writer,status = status )
            post.save(force_insert=True)
            for category in category_field:
                post.category.add(category)
            
            
            context = {
             "form" : AddPostForm
            }
            messages.success(request,"post submit")
            return render(request,"account/dash/addpost.html",context)
        else:
            messages.error(request,"error")
            context = {
             "form" : AddPostForm
            }
            return render(request,"account/dash/addpost.html",context)
    else:
        context = {
             "form" : AddPostForm
            }
        return render(request,"account/dash/addpost.html",context)

def update_post(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    form = UpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        if request.user.is_superuser :
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
        else :
            instance = form.save(commit=False)
            instance.status = "d"
            instance.save()
            form.save_m2m()
        messages.success(request, "Post Saved")
        context = {
                    
                    "form":form
            }
        return render(request, "account/dash/addpost.html", context)
    else:
        context = {
                    
                    "form":form
            }

        return render(request, "account/dash/addpost.html", context)
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post,slug = slug)
    post.delete()
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    return render(request,"account/dash/dash.html",context)
        