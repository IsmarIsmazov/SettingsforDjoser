from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.core.mail import send_mail

# Create your views here.

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.validated_data['username'])
        self.send_email_confirmation(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def send_email_confirmation(self, user):
        subject = 'Подтверждение регистрации'
        message = f'Привет, {user.username}! Пожалуйста, подтвердите свой email по ссылке: https://t.me/Savadatsu'
        from_email = 'registerdrf@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)