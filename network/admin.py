from django.contrib import admin
from .models import Post, User

admin.site.register(Post)
admin.site.register(User)

admin.site.site_header  =  "Social Media Admin"  
admin.site.site_title  =  "Social Media Admin"
admin.site.index_title  =  "Social Media Admin"
# Register your models here.
