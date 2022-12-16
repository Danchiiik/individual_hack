from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.account.tasks import send_act_code_celery

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=4, required=True, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        
         
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')
        
        if p1 != p2:
            raise serializers.ValidationError('Passwords are not similar')
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        code = user.activation_code
        send_act_code_celery.delay(user.email, code)
        user.save()
        return user
        
        

