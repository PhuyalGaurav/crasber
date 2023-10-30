from django.contrib import admin
from .models import Post

admin.site.register(Post)

admin.site.site_header  =  "Social Media Admin"  
admin.site.site_title  =  "Social Media Admin"
admin.site.index_title  =  "Social Media Admin"
# Register your models here.
