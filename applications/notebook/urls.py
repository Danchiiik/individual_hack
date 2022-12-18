from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.notebook.views import CommentApiView, NotebookApiView, OrderActivateApiView, OrderApiView

router = DefaultRouter()
router.register('buy', OrderApiView)
router.register('comment', CommentApiView)
router.register('', NotebookApiView)

urlpatterns = [
    path('buy/<uuid:order_code>/', OrderActivateApiView.as_view())
]

urlpatterns += router.urls
