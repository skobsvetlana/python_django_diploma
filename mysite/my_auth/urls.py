from django.urls import path, include

from my_auth.views import (LoginViewSet,
                           UserRegistrationViewSet,
                           LogoutViewSet,
                           )

from rest_framework.routers import DefaultRouter

app_name = "my_auth"

routers = DefaultRouter()

routers.register("sign-in", LoginViewSet, basename="sign-in")
routers.register("sign-up", UserRegistrationViewSet, basename="sign-up")
routers.register("sign-out", LogoutViewSet, basename="sign-out")


urlpatterns = [
    path("", include(routers.urls)),
    path("sign-out", LogoutViewSet.as_view({'post': 'update'})),
    path("sign-in", LoginViewSet.as_view({'post': 'create'})),
    path("sign-up", UserRegistrationViewSet.as_view({'post': 'create'})),
]