from django.urls import path, include

from my_auth.views import AuthViewSet

from rest_framework.routers import DefaultRouter

app_name = "my_auth"

routers = DefaultRouter()

routers.register("my_auth", AuthViewSet, basename="user_auth")

urlpatterns = [
    path("", include(routers.urls)),
    path("sign-out", AuthViewSet.as_view({'post': 'logout'})),
    path("sign-in", AuthViewSet.as_view({'post': 'login'})),
]