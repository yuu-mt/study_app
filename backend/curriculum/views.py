from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChapterProgress, CurriculumChapter, CurriculumItem, TraineeProfile
from .permissions import IsAdminOrReadOnlyForInstructor, IsAdminRole, IsInstructorOrAdmin
from .serializers import (
    ChapterReorderSerializer,
    CurriculumChapterOptionSerializer,
    CurriculumChapterSerializer,
    CurriculumItemSerializer,
    InstructorRegisterSerializer,
    TraineeDetailSerializer,
    TraineeListSerializer,
    TraineeRegisterSerializer,
    TraineeStatusUpdateSerializer,
    UserCandidateSerializer,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# 章選択UI用（受講生側：学習タイマー・振り返り画面）要件4-3・4-4
# 全ロールの認証済みユーザーが閲覧可能（instructor/adminに限定しない）
# ---------------------------------------------------------------------------

class CurriculumChapterOptionsView(generics.ListAPIView):
    """章選択の選択肢一覧（表示順）。受講生自身が学習タイマー・振り返り画面で使用する。
    各章に紐づく小項目もあわせて返す。
    """
    queryset = CurriculumChapter.objects.prefetch_related('items').order_by('order')
    serializer_class = CurriculumChapterOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


# ---------------------------------------------------------------------------
# 受講生一覧・登録・進捗管理（要件 3-1-a, 3-1-b, 3-1-c, 3-4）
# ---------------------------------------------------------------------------

class TraineeListView(generics.ListAPIView):
    """受講生一覧取得API。担当の有無に関わらず全講師が全受講生を閲覧できる（要件3-1-a）"""
    serializer_class = TraineeListSerializer
    permission_classes = [IsInstructorOrAdmin]
    pagination_class = None

    def get_queryset(self):
        queryset = TraineeProfile.objects.select_related('user', 'mentor').all()
        status_filter = self.request.query_params.get('status')
        if status_filter and status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
        return queryset


class TraineeRegisterView(generics.CreateAPIView):
    """受講生登録API：既存アプリユーザーを選択してtraineeロールを付与する（要件3-1-b）"""
    serializer_class = TraineeRegisterSerializer
    permission_classes = [IsInstructorOrAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trainee = serializer.save()
        return Response(
            TraineeDetailSerializer(trainee).data, status=status.HTTP_201_CREATED
        )


class TraineeCandidateListView(generics.ListAPIView):
    """受講生登録画面用：まだ受講生登録されていないアプリユーザー一覧（要件3-1-b）"""
    serializer_class = UserCandidateSerializer
    permission_classes = [IsInstructorOrAdmin]
    pagination_class = None

    def get_queryset(self):
        queryset = User.objects.filter(trainee_profile__isnull=True)
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )
        return queryset


class MentorListView(generics.ListAPIView):
    """受講生登録画面の「担当メンバー」選択用：instructor/adminロールのユーザー一覧"""
    serializer_class = UserCandidateSerializer
    permission_classes = [IsInstructorOrAdmin]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(role__in=['instructor', 'admin'])


class InstructorCandidateListView(generics.ListAPIView):
    """講師登録画面用：まだinstructor/adminロールを持たないユーザー一覧（adminのみ閲覧可）"""
    serializer_class = UserCandidateSerializer
    permission_classes = [IsAdminRole]
    pagination_class = None

    def get_queryset(self):
        queryset = User.objects.exclude(role__in=['instructor', 'admin'])
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )
        return queryset


class TraineeDetailView(generics.RetrieveAPIView):
    """進捗管理（受講生詳細画面）：現在の章・完了状況・累計学習時間・振り返り記録（要件3-1-c）"""
    queryset = TraineeProfile.objects.select_related('user', 'mentor').prefetch_related(
        'chapter_progresses__chapter'
    )
    serializer_class = TraineeDetailSerializer
    permission_classes = [IsInstructorOrAdmin]


class TraineeStatusUpdateView(APIView):
    """受講生一覧からのステータス変更API（未受講→受講中→完了）（要件3-1-a・3-4）"""
    permission_classes = [IsInstructorOrAdmin]

    def patch(self, request, pk):
        try:
            trainee = TraineeProfile.objects.get(pk=pk)
        except TraineeProfile.DoesNotExist:
            return Response({'error': '受講生が見つかりません'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TraineeStatusUpdateSerializer(instance=trainee, data=request.data)
        serializer.is_valid(raise_exception=True)
        trainee = serializer.save()
        return Response(TraineeDetailSerializer(trainee).data)


# ---------------------------------------------------------------------------
# 講師ロール付与（adminのみ、要件3-1-b・v3確定No.3）
# ---------------------------------------------------------------------------

class InstructorRegisterView(generics.CreateAPIView):
    """講師（instructor）ロール付与API。adminアカウントのみ実行可能"""
    serializer_class = InstructorRegisterSerializer
    permission_classes = [IsAdminRole]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'id': user.id, 'username': user.username, 'role': user.role},
            status=status.HTTP_201_CREATED,
        )


# ---------------------------------------------------------------------------
# カリキュラム管理画面（要件3-3）：instructorは閲覧のみ、adminは編集・削除・並び替え可能
# ---------------------------------------------------------------------------

class CurriculumChapterListCreateView(generics.ListCreateAPIView):
    """カリキュラム一覧取得・新規追加API（要件3-3-a・3-3-b）"""
    queryset = CurriculumChapter.objects.prefetch_related('items').all()
    serializer_class = CurriculumChapterSerializer
    permission_classes = [IsAdminOrReadOnlyForInstructor]
    pagination_class = None


class CurriculumChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """カリキュラム章の編集・削除API（要件3-3-c・3-3-d）"""
    queryset = CurriculumChapter.objects.prefetch_related('items').all()
    serializer_class = CurriculumChapterSerializer
    permission_classes = [IsAdminOrReadOnlyForInstructor]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 進捗記録(chapter_progress)が既に存在する章は削除不可とする（要件3-3-d）
        if ChapterProgress.objects.filter(chapter=instance).exists():
            return Response(
                {'error': 'この章には受講生の進捗記録が存在するため削除できません'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class CurriculumChapterReorderView(APIView):
    """カリキュラム章の並び替えAPI（ドラッグ&ドロップ／上下ボタン）（要件3-3-a）"""
    permission_classes = [IsAdminRole]

    def patch(self, request):
        serializer = ChapterReorderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        chapters_by_id = {c.id: c for c in CurriculumChapter.objects.filter(
            id__in=[item['id'] for item in serializer.validated_data]
        )}
        missing_ids = [
            item['id'] for item in serializer.validated_data if item['id'] not in chapters_by_id
        ]
        if missing_ids:
            return Response(
                {'error': f'章が見つかりません: {missing_ids}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated = []
        for item in serializer.validated_data:
            chapter = chapters_by_id[item['id']]
            chapter.order = item['order']
            updated.append(chapter)
        CurriculumChapter.objects.bulk_update(updated, ['order'])

        chapters = CurriculumChapter.objects.prefetch_related('items').order_by('order')
        return Response(CurriculumChapterSerializer(chapters, many=True).data)


# ---------------------------------------------------------------------------
# カリキュラム小項目管理（要件3-3・v3.3追加）：章と同様、instructorは閲覧のみ
# ---------------------------------------------------------------------------

class CurriculumItemListCreateView(generics.ListCreateAPIView):
    """指定した章に紐づく小項目の一覧取得・新規追加API"""
    serializer_class = CurriculumItemSerializer
    permission_classes = [IsAdminOrReadOnlyForInstructor]
    pagination_class = None

    def get_queryset(self):
        return CurriculumItem.objects.filter(chapter_id=self.kwargs['chapter_id']).order_by('order')

    def perform_create(self, serializer):
        chapter = generics.get_object_or_404(CurriculumChapter, id=self.kwargs['chapter_id'])
        serializer.save(chapter=chapter)


class CurriculumItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """小項目の編集・削除API"""
    queryset = CurriculumItem.objects.all()
    serializer_class = CurriculumItemSerializer
    permission_classes = [IsAdminOrReadOnlyForInstructor]
