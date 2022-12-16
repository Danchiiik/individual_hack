from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.notebook.views import CommentApiView, NotebookApiView

router = DefaultRouter()
router.register('comment', CommentApiView)
router.register('', NotebookApiView)

urlpatterns = []

urlpatterns += router.urls
