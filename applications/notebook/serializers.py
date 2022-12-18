from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()

from applications.notebook.models import Comment, Favourite, Image, Notebook, Order, Rating
from applications.notebook.tasks import send_order_confirm



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



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
        rep['favourites'] = instance.favourites.filter(favourite=True).count()
        return rep
    
    def create(self, validated_data):
        request = self.context.get('request')
        files_data = request.FILES
        notebook_obj = Notebook.objects.create(**validated_data)
        for image in files_data.getlist('images'):
            Image.objects.create(notebook_obj=notebook_obj, image=image)  
        return notebook_obj
 
    
    
class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=10)
    class Meta:
        model = Rating
        fields = ['rating']
  
        

class FavouriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Favourite
        fields = '__all__'
        
    
        
class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    amount = serializers.IntegerField(required=True)
    class Meta:
        model = Order
        fields = '__all__'
        
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_order_code()
        order.save()
        send_order_confirm.delay(order.owner.email, order.order_code)
        return order
     
    def validate(self, attrs):
        notebook_obj = attrs['notebook_obj']
        amount = attrs['amount']
        if notebook_obj.amount < amount:
            raise serializers.ValidationError(f'Soory, but we have only {notebook_obj.amount} pcs')
        return attrs
        
             
    
        
        
        
        
        
    
        
        
        
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     user.set_password(validated_data['password'])
    #     code = user.activation_code
    #     send_act_code_celery.delay(user.email, code)
    #     user.save()
    #     return user    