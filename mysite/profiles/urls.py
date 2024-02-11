from django.urls import path, include

from profiles.views import UserProfileViewset, AvatarUpdateViewset

from rest_framework.routers import DefaultRouter

app_name = "profiles"

routers = DefaultRouter()

routers.register("profile", UserProfileViewset, basename="profile")

urlpatterns = [
    path("", include(routers.urls)),
    path("profile", UserProfileViewset.as_view({'get': 'retrieve',
                                                'post': 'update',
                                                 })),
    path("profile/avatar", AvatarUpdateViewset.as_view({'post': 'update'})),
]