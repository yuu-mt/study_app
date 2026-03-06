from django.urls import path
from .views import (
    CategoryListView,
    StudyRecordListCreateView,
    StudyRecordDetailView,
    StudySummaryView,
    StampView,
)

urlpatterns = [
    # カテゴリー一覧
    path('categories/', CategoryListView.as_view(), name='categories'),
    # 学習記録一覧・新規作成
    path('records/', StudyRecordListCreateView.as_view(), name='study_records'),
    # 学習記録詳細・更新・削除
    path('records/<int:pk>/', StudyRecordDetailView.as_view(), name='study_record_detail'),
    # 学習時間集計
    path('summary/', StudySummaryView.as_view(), name='study_summary'),
    # スタンプ
    path('records/<int:record_id>/stamp/', StampView.as_view(), name='stamp'),
]