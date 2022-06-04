#==>Library Import
from django.contrib import admin
#==>Local Import
from .models import Post, Category, IPAddress, Like, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_categories', 'jcreated', 'status')
    list_per_page = 10
    list_editable = ('status',)



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(IPAddress)
admin.site.register(Like)
admin.site.register(Comment)