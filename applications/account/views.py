from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

from applications.account.serializers import UserSerializer


class UserRegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response('We have sent you an activation code to your email!')



class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'wrong code'}, status=status.HTTP_400_BAD_REQUEST)
    