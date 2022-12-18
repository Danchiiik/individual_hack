from django.contrib import admin
from django.db.models import Avg

from applications.notebook.models import Image, Notebook, Order

class ImageAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 10


class NotebookAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'rating' ,'likes', 'favourites']
    inlines = [ImageAdmin]
    
    def likes(self, obj):
        return obj.likes.filter(like=True).count()
    
    def favourites(self, obj):
        return obj.favourites.filter(favourite=True).count()
    
    def rating(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']
    
    
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Image)
admin.site.register(Order)