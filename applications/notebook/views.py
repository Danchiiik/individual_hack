from rest_framework.viewsets import mixins, GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from applications.notebook.models import Comment, Favourite, Like, Notebook, Rating
from applications.notebook.serializers import CommentSerializer, FavouriteSerializer, NotebookSerializer, RatingSerializer
from applications.notebook.permissions import IsOwner, IsCommentOwner


# page settings
class PaginationApiView(PageNumberPagination):
    page_size = 5
    max_page_size = 100
    page_size_query_param = 'notebooks_page'
    
    
class NotebookApiView(
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer
    permission_classes = [IsOwner]
    pagination_class = PaginationApiView
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'brand', 'price']
    search_fields = ['name', 'brand']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):
        try:
            like_na_nout, _ = Like.objects.get_or_create(notebook_obj_id=pk, owner=request.user)
            like_na_nout.like = not like_na_nout.like
            like_na_nout.save()
            status = 'liked'
            if not like_na_nout.like:
                status = 'unliked'
            return Response(f'You {status} this notebook')
        except:
            return Response('Something went wrong, please check if your operation is correct')
    
    
    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rating_na_nout, _ = Rating.objects.get_or_create(notebook_obj_id=pk, owner=request.user)
            rating_na_nout.rating = request.data['rating']
            rating_na_nout.save()
            return Response(f'You give {request.data["rating"]} points to this notebook')
        except:
            return Response('Something went wrong, please check if your operation is correct')


    @action(detail=True, methods=['POST'])
    def favourite(self, request, pk, *args, **kwargs):
        try:
            love_na_nout, _ = Favourite.objects.get_or_create(notebook_obj_id=pk, owner=request.user)
            love_na_nout.favourite = not love_na_nout.favourite
            love_na_nout.save()
            status = 'saved'
            if not love_na_nout.favourite:
                status = 'unsaved'
            return Response(f'You {status} this notebook to your favourites')
        except:
            return Response('Something went wrong, please check if your operation is correct')
    
    
class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
        
    
    
    
