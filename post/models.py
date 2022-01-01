from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 

# Create your models here.
class PublishManager(models.Manager):
    def publish(self):
        return self.filter(status = "p")
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.title

    
class Post(models.Model):
    choise_status =(("p","Publish"),("d","Draft"))
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = RichTextUploadingField ()
    image = models.ImageField(upload_to= "media",blank=True, null=True)
    category = models.ManyToManyField(Category,related_name="postcategory")
    writer = models.ForeignKey(get_user_model(),on_delete=CASCADE)
    status = models.CharField(choices=choise_status,max_length=2)
    create = models.DateTimeField(auto_now_add=True)
    objects = PublishManager()
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-create']
    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})
    
    