from django.urls import path

from .views import (
    CurriculumChapterDetailView,
    CurriculumChapterListCreateView,
    CurriculumChapterOptionsView,
    CurriculumChapterReorderView,
    InstructorCandidateListView,
    InstructorRegisterView,
    MentorListView,
    TraineeCandidateListView,
    TraineeDetailView,
    TraineeListView,
    TraineeRegisterView,
    TraineeStatusUpdateView,
)

urlpatterns = [
    # 受講生一覧・登録
    path('trainees/', TraineeListView.as_view(), name='trainee_list'),
    path('trainees/register/', TraineeRegisterView.as_view(), name='trainee_register'),
    path('trainees/candidates/', TraineeCandidateListView.as_view(), name='trainee_candidates'),
    # 受講生詳細（進捗管理）・ステータス変更
    path('trainees/<int:pk>/', TraineeDetailView.as_view(), name='trainee_detail'),
    path('trainees/<int:pk>/status/', TraineeStatusUpdateView.as_view(), name='trainee_status_update'),
    # 担当メンバー（instructor/admin）一覧・講師ロール付与（adminのみ）
    path('mentors/', MentorListView.as_view(), name='mentor_list'),
    path('instructors/candidates/', InstructorCandidateListView.as_view(), name='instructor_candidates'),
    path('instructors/register/', InstructorRegisterView.as_view(), name='instructor_register'),
    # 受講生側の章選択UI用（全ロール閲覧可）
    path('chapters/options/', CurriculumChapterOptionsView.as_view(), name='chapter_options'),
    # カリキュラム管理
    path('chapters/', CurriculumChapterListCreateView.as_view(), name='chapter_list'),
    path('chapters/<int:pk>/', CurriculumChapterDetailView.as_view(), name='chapter_detail'),
    path('chapters/reorder/', CurriculumChapterReorderView.as_view(), name='chapter_reorder'),
]
