from django.contrib import admin
from django.db.models import Avg

from applications.notebook.models import Notebook

class NotebookAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'rating_notebook' ,'notebook_count_like']
    
    
    def notebook_count_like(self, obj):
        return obj.likes.filter(like=True).count()
    
    def rating_notebook(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']
    


admin.site.register(Notebook, NotebookAdmin)