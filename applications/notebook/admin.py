from django.contrib import admin
from django.db.models import Avg

from applications.notebook.models import Image, Notebook

class ImageAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 10


class NotebookAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'rating_notebook' ,'notebook_count_like', 'notebook_count_favourites']
    inlines = [ImageAdmin]
    
    def notebook_count_like(self, obj):
        return obj.likes.filter(like=True).count()
    
    def notebook_count_favourites(self, obj):
        return obj.favourites.filter(favourite=True).count()
    
    def rating_notebook(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']
    
    
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Image)