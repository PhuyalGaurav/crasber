from django.contrib import admin
from .models import Post, User

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'likes', 'edited')
    list_display_links = ('id', 'user', )
    search_fields = ('content',)
    list_editable = ('likes', 'edited')
    list_filter = ('edited', 'user')


admin.site.register(Post, PostAdmin)
admin.site.register(User)

admin.site.site_header  =  "Social Media Admin"  
admin.site.site_title  =  "Social Media Admin"
admin.site.index_title  =  "Social Media Admin"
# Register your models here.
