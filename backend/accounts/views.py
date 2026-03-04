from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """新規登録API"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_class = [permissions.AllowAny] # 未ログインでもアクセス可

class UserDetailView(generics.RetrieveUpdateAPIView):
    """ログイン中のユーザー情報取得・更新API"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # ログイン必須

    def get_object(self):
        return self.request.user # ログイン中のユーザーを返す
    
class LogoutView(APIView):
    """ログアウトAPI"""
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist() # トークンを無効化
            return Response({'message': 'ログアウトしました'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': '無効なトークンです'}, status=status.HTTP_400_BAD_REQUEST)