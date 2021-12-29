from django.contrib import admin

from post.models import Category, Post

# Register your models here.
class adminpro(admin.ModelAdmin):
    list_display = ('title','writer','status','create')
    list_filter = ('status', 'create')
    search_fields = ('title','body')
    list_editable = ('status',)
    ordering = ['-create']
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(Category)
admin.site.register(Post,adminpro)

