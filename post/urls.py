from django.urls import path

from post.views import search, show_post_detail, show_posts

app_name = "post"
urlpatterns = [
    path('', show_posts, name = "index"),
    path('category/<str:cat_list>', show_posts, name = "cat"),
    path('writer/<str:writer>', show_posts, name = "writer"),
    path('search', search, name = "search"),
    path('post/<slug:slug>', show_post_detail, name = "detail"),
    

]