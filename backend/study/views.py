from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Category, StudyRecord, Stamp
from .serializers import CategorySerializer, StudyRecordSerializer, StampSerializer


class CategoryListView(generics.ListAPIView):
    """カテゴリー一覧取得API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class StudyRecordListCreateView(generics.ListCreateAPIView):
    """学習記録一覧取得・新規作成API"""
    serializer_class = StudyRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StudyRecord.objects.filter(user=self.request.user)
        # カテゴリーで絞り込み
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def perform_create(self, serializer):
        # 保存時に自動でログイン中のユーザーをセット
        serializer.save(user=self.request.user)


class StudyRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """学習記録詳細・更新・削除API"""
    serializer_class = StudyRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 自分の記録のみ操作可能
        return StudyRecord.objects.filter(user=self.request.user)


class StudySummaryView(APIView):
    """学習時間集計API（週間・月間）"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # 週間集計（今日から7日前）
        week_start = today - timedelta(days=6)
        weekly = StudyRecord.objects.filter(
            user=request.user,
            study_date__gte=week_start,
            study_date__lte=today
        ).aggregate(total=Sum('duration_minutes'))

        # 月間集計（今月1日から今日）
        month_start = today.replace(day=1)
        monthly = StudyRecord.objects.filter(
            user=request.user,
            study_date__gte=month_start,
            study_date__lte=today
        ).aggregate(total=Sum('duration_minutes'))

        # 連続学習日数
        streak = self.calculate_streak(request.user, today)

        return Response({
            'weekly_minutes': weekly['total'] or 0,
            'monthly_minutes': monthly['total'] or 0,
            'streak_days': streak,
        })

    def calculate_streak(self, user, today):
        streak = 0
        check_date = today
        while True:
            exists = StudyRecord.objects.filter(
                user=user,
                study_date=check_date
            ).exists()
            if exists:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        return streak


class StampView(APIView):
    """スタンプ送信・取り消しAPI"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, record_id):
        try:
            record = StudyRecord.objects.get(id=record_id)
        except StudyRecord.DoesNotExist:
            return Response({'error': '記録が見つかりません'}, status=status.HTTP_404_NOT_FOUND)

        stamp_type = request.data.get('stamp_type', 'good')
        stamp, created = Stamp.objects.get_or_create(
            from_user=request.user,
            study_record=record,
            defaults={'stamp_type': stamp_type}
        )

        if created:
            return Response({'message': 'スタンプを送りました', 'stamp_type': stamp_type}, status=status.HTTP_201_CREATED)
        else:
            # すでにスタンプ済みなら取り消し
            stamp.delete()
            return Response({'message': 'スタンプを取り消しました'}, status=status.HTTP_200_OK)

class WeeklyChartView(APIView):
    """週間グラフ用データAPI"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        result = []

        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            total = StudyRecord.objects.filter(
            user=request.user,
            study_date=date
        ).aggregate(total=Sum('duration_minutes'))['total'] or 0

            result.append({
                'date': date.strftime('%m/%d'),
                'minutes': total
        })

        return Response(result)