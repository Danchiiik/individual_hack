from rest_framework import serializers
from django.db.models import Avg

from applications.notebook.models import Comment, Notebook, Rating


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Comment
        fields = '__all__'


class NotebookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Notebook
        fields = '__all__'
    
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.filter(like=True).count()
        rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
    
        return rep
    
    
class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=10)
    class Meta:
        model = Rating
        fields = ['rating']
        
    
        
        
        