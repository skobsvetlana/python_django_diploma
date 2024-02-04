from django.contrib.auth import login, logout, authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

class AuthViewSet(GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    def login(self, request):
        data = next(iter(request.data.keys()))
        print("ghgjgjgjgj", data, type(data))

        # username = data.get("username")
        # password = data.get("password")

        username = "admin"
        password = "1234"

        if username and password:
            user = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if not user:
                msg = 'Access denied: wrong username or password.'
                return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            msg = 'Both "username" and "password" are required.'
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        login(request=request, user=user)

        return Response({"message": "Logged in successfully"}, status=status.HTTP_202_ACCEPTED)


    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    # class RegisterView(CreateView):
    #     form_class = UserCreationForm
    #
    #     def form_valid(self, form):
    #         response = super().form_valid(form)
    #         Profile.objects.create(user=self.object)
    #
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password1")
    #         user = authenticate(
    #             self.request,
    #             username=username,
    #             password=password,
    #         )
    #         login(request=self.request, user=user)
    #
    #         return response



