from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, \
    DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .models import BaseUser
from .serializers import baseUserSerial, createUserSerial
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        '用户列表': reverse('user_list', request=request, format=format),
        '用户个人信息': reverse('user_info', request=request, format=format),
        '用户申请账号': reverse('create_user', request=request, format=format),
    })

# Create your views here.

class ObtainExpiringAuthToken(ObtainAuthToken):
    """
    每次登录刷新token的创建时间
    """

    def post(self, request, *args, **kwargs):
        print('login')
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        if user.delete_status:
            return Response({"error": '已被删除'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        return Response({'token': token.key})


obtain_auth_token = ObtainExpiringAuthToken.as_view()


class AllUsers(ListAPIView):
    serializer_class = baseUserSerial
    permission_classes = [permissions.IsAuthenticated]
    queryset = BaseUser.objects.all()


class UsersInfo(RetrieveAPIView):
    serializer_class = baseUserSerial
    permission_classes = [IsAuthenticated]
    queryset = BaseUser.objects.all()

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        # print(serializer.data)
        return Response(serializer.data)


class CreateUsers(CreateAPIView):
    serializer_class = createUserSerial

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validate(request.data):
                self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
