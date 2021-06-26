from rest_framework.views import APIView
from backend.services.auth import *


class SignInView(APIView):

    def post(self, request):
        return sign_in(request)


class LoginView(APIView):

    def post(self, request):
        return login(request)



