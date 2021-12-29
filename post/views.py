from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from post.models import Category, Post

# Create your views here.
def show_posts(request,cat_list= None, writer = None):
    if cat_list != None:
        posts = Post.objects.publish().filter(category__title =cat_list )
        cat = Category.objects.all()
        context = {
            "posts" : posts,
            "cats" : cat
        }
        return render(request,"post/index.html",context)
    elif writer != None:
        posts = Post.objects.filter(writer__email = writer)
        cat = Category.objects.all()
        context = {
            "posts" : posts,
            "cats" : cat
        }
        return render(request,"post/index.html",context)
    else:
        posts = Post.objects.publish()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        cat = Category.objects.all()
        context = {
            "posts" : page_obj,
            "cats" : cat,
           
        }
        return render(request,"post/index.html",context)
    
    
def show_post_detail(request , slug):
    post_detail = get_object_or_404(Post,slug = slug)
    cat = Category.objects.all()
    context = {
            "post_detail" : post_detail,
            "cats" : cat
        }
    return render(request,"post/post.html",context)

def search(request):       
    cat = Category.objects.all() 
    if request.method == 'GET': 
        title_search =  request.GET.get('search') 
        posts = Post.objects.filter(Q(title__icontains=title_search) | Q(body__icontains=title_search))
        context = {
            "posts" : posts,
            "cats" : cat
        }
        return render(request,"post/index.html",context)
