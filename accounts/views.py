from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return Response({"message": "Login exitoso", "user_id": user.id, "role": user.role})
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)