from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from profiles.serializers import ProfileSerializer
from profiles.models import Profile

class UserProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user").all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        item = get_object_or_404(self.queryset, user=request.user)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++profile_retrieve")
        print("data", serializer.data)

        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs) -> Response:
        pass

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)



