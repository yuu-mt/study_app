from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserSerializer
from .models import Friendship
from django.contrib.auth import get_user_model

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
        
class FriendListView(generics.ListAPIView):
    """友達一覧取得API"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            followers__from_user=self.request.user
        )


class FriendRequestView(APIView):
    """友達追加・削除API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'ユーザーが見つかりません'}, status=status.HTTP_404_NOT_FOUND)

        if to_user == request.user:
            return Response({'error': '自分自身は追加できません'}, status=status.HTTP_400_BAD_REQUEST)

        friendship, created = Friendship.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

        if created:
            return Response({'message': f'{to_user.username}を友達追加しました'}, status=status.HTTP_201_CREATED)
        else:
            friendship.delete()
            return Response({'message': f'{to_user.username}を友達削除しました'}, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    """ユーザー検索API"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return User.objects.filter(
                username__icontains=query
            ).exclude(id=self.request.user.id)
        return User.objects.none()
