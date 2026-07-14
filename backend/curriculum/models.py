from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class CurriculumChapter(models.Model):
    """カリキュラムマスタ（章）

    要件定義 3-3・5-3参照。adminアカウントが管理画面から登録・編集・並び替え・削除する。
    """
    chapter_number = models.CharField(
        max_length=10, unique=True, verbose_name='章番号'
    )  # 例: "00", "01" ... "13"（表示上のラベル。並び順は order フィールドで管理）
    title = models.CharField(max_length=200, verbose_name='章タイトル')
    estimated_days = models.PositiveIntegerField(verbose_name='想定日数')
    order = models.PositiveIntegerField(default=0, verbose_name='表示順')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カリキュラム章'
        verbose_name_plural = 'カリキュラム章'
        ordering = ['order']

    def __str__(self):
        return f'{self.chapter_number} {self.title}'


class CurriculumItem(models.Model):
    """カリキュラムマスタ（章ごとの小項目）

    要件定義 3-3・5-3・5-4参照（v3.3追加）。
    """
    chapter = models.ForeignKey(
        CurriculumChapter,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='章'
    )
    item_number = models.CharField(max_length=10, verbose_name='項目番号')
    title = models.CharField(max_length=200, verbose_name='項目名')
    order = models.PositiveIntegerField(default=0, verbose_name='表示順')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カリキュラム項目'
        verbose_name_plural = 'カリキュラム項目'
        ordering = ['order']
        unique_together = ('chapter', 'item_number')

    def __str__(self):
        return f'{self.chapter.chapter_number}-{self.item_number} {self.title}'


class TraineeProfile(models.Model):
    """受講生プロフィール（管理画面上の受講生管理情報）

    要件定義 3-1-a・3-1-b・3-4・5-3参照。
    """
    STATUS_NOT_STARTED = 'not_started'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, '未受講'),
        (STATUS_IN_PROGRESS, '受講中'),
        (STATUS_COMPLETED, '完了'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trainee_profile',
        verbose_name='ユーザー'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
        verbose_name='ステータス'
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentoring_trainees',
        verbose_name='担当メンバー'
    )
    start_date = models.DateField(
        null=True, blank=True, verbose_name='学習開始日'
    )  # 「受講中」への変更時に手動入力（要件 3-4 ステップ③）
    expected_end_date = models.DateField(
        null=True, blank=True, verbose_name='完了予定日'
    )  # 学習開始日 + 全章の想定日数合計から自動算出（要件 3-1-b）

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '受講生プロフィール'
        verbose_name_plural = '受講生プロフィール'

    def __str__(self):
        return f'{self.user.username}（{self.get_status_display()}）'

    def calculate_expected_end_date(self):
        """学習開始日 + 全カリキュラム章の想定日数合計から完了予定日を算出する"""
        if not self.start_date:
            return None
        total_days = CurriculumChapter.objects.aggregate(
            total=models.Sum('estimated_days')
        )['total'] or 0
        return self.start_date + timedelta(days=total_days)

    def get_current_chapter(self):
        """現在取り組んでいる章（未完了の中で最も表示順が早い章）を返す（要件3-1-a）"""
        if self.status != self.STATUS_IN_PROGRESS:
            return None
        completed_ids = self.chapter_progresses.filter(
            is_completed=True
        ).values_list('chapter_id', flat=True)
        return CurriculumChapter.objects.exclude(id__in=completed_ids).order_by('order').first()

    def get_chapter_due_date(self, chapter):
        """指定した章の完了予定日（学習開始日 + その章までの想定日数累計）を返す（要件3確定No.1）"""
        if not self.start_date or not chapter:
            return None
        cumulative_days = CurriculumChapter.objects.filter(
            order__lte=chapter.order
        ).aggregate(total=models.Sum('estimated_days'))['total'] or 0
        return self.start_date + timedelta(days=cumulative_days)

    def is_delayed(self):
        """現在の章の完了予定日から1日超過しても未完了の場合Trueを返す（要件3確定No.1）"""
        if self.status != self.STATUS_IN_PROGRESS:
            return False
        chapter = self.get_current_chapter()
        due_date = self.get_chapter_due_date(chapter)
        if not due_date:
            return False
        return (timezone.now().date() - due_date).days >= 1


class ChapterProgress(models.Model):
    """受講生ごとの章別進捗

    要件定義 3-2・4-4・5-3参照。完了は受講生自身の操作のみで確定する（講師承認なし）。
    """
    trainee = models.ForeignKey(
        TraineeProfile,
        on_delete=models.CASCADE,
        related_name='chapter_progresses',
        verbose_name='受講生'
    )
    chapter = models.ForeignKey(
        CurriculumChapter,
        on_delete=models.CASCADE,
        related_name='progresses',
        verbose_name='章'
    )
    is_completed = models.BooleanField(default=False, verbose_name='完了フラグ')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完了日時')
    total_minutes = models.PositiveIntegerField(default=0, verbose_name='累計学習時間（分）')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '章別進捗'
        verbose_name_plural = '章別進捗'
        unique_together = ('trainee', 'chapter')

    def __str__(self):
        status = '完了' if self.is_completed else '未完了'
        return f'{self.trainee.user.username} - {self.chapter.chapter_number}（{status}）'
