from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, User
from .permissions import IsUserOrReadOnly
from .serializers import ProfileSerializer, UserSerializer


class UserList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
