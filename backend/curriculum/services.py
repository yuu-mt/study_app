from django.db.models import Sum
from django.utils import timezone

from .models import ChapterProgress


def sync_chapter_progress(record):
    """学習記録(StudyRecord)がカリキュラムカテゴリー・章選択付きで保存された際に、
    対応するChapterProgressの累計学習時間を再集計し、
    「完了」ボタン押下（is_chapter_completion）の場合は完了状態にする（要件3-2・4-3・4-4）。

    冪等性のため、累計学習時間は都度「対象章・対象ユーザーの全記録」から再計算する
    （新規作成時・振り返り画面での更新時のどちらから呼ばれても二重加算しない）。

    受講生登録（TraineeProfile）がまだ行われていないユーザーの記録は対象外とする。
    """
    if not record.category or record.category.name != 'curriculum':
        return
    if not record.chapter:
        return
    trainee_profile = getattr(record.user, 'trainee_profile', None)
    if not trainee_profile:
        return

    from study.models import StudyRecord

    progress, _ = ChapterProgress.objects.get_or_create(
        trainee=trainee_profile, chapter=record.chapter
    )
    total_minutes = StudyRecord.objects.filter(
        user=record.user, chapter=record.chapter, category__name='curriculum'
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0
    progress.total_minutes = total_minutes

    if record.is_chapter_completion and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()

    progress.save()
