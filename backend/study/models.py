from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """カテゴリーマスター"""
    CATEGORY_CHOICE = [
        ('tech', '技術'),
        ('culture', '教養'),
        ('license', '資格'),
        ('curriculum', 'カリキュラム'),
    ]
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICE, unique=True, verbose_name='カテゴリー名')

    class Meta:
        verbose_name = 'カテゴリー'

    def __str__(self):
        return self.get_name_display()


class StudyRecord(models.Model):
    """学習記録モデル"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_records',
        verbose_name='ユーザー'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='カテゴリー'
    )
    # カテゴリーが「カリキュラム」の場合のみ入力される章選択（要件 4-3・4-4）。
    # is_curriculum相当の判定は category.name == 'curriculum' で行うため、独立フラグは持たない。
    chapter = models.ForeignKey(
        'curriculum.CurriculumChapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_records',
        verbose_name='対象章'
    )
    # 対象章に紐づく小項目（curriculum_item）の選択。任意項目（章によっては小項目が無い場合もあるため）。
    item = models.ForeignKey(
        'curriculum.CurriculumItem',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_records',
        verbose_name='対象小項目'
    )
    title = models.CharField(max_length=200, verbose_name='学習タイトル')
    description = models.TextField(blank=True, verbose_name='学習詳細')
    study_date = models.DateField(verbose_name='学習日')
    duration_minutes = models.PositiveIntegerField(verbose_name='学習時間（分）')
    understanding = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='理解度'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #振り返りフィールド
    questions = models.TextField(blank=True, null=True, verbose_name='問題点/疑問点')
    struggles = models.TextField(blank=True, null=True, verbose_name='難しかったこと')
    achievements = models.TextField(blank=True, null=True, verbose_name='できるようになったこと')
    solutions = models.TextField(blank=True, null=True, verbose_name='解決に向けて行ったこと')

    # 振り返り記録入力画面の「完了」ボタン押下を表すフラグ（要件 3-2・4-4）。
    # True の場合、対応する ChapterProgress を完了済みとして記録する。
    is_chapter_completion = models.BooleanField(default=False, verbose_name='章完了操作')

    class Meta:
        verbose_name = '学習記録'
        ordering = ['-study_date', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.title} ({self.study_date})'


class Stamp(models.Model):
    """いいねモデル"""
    STAMP_CHOICES = [
        ('good', '👍'),
        ('great', '🔥'),
        ('nice', '💖')
    ] 
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_stamps',
        verbose_name='送ったユーザー'
    )
    study_record = models.ForeignKey(
        StudyRecord,
        on_delete=models.CASCADE,
        related_name='stamps',
        verbose_name='学習記録'
    )
    stamp_type = models.CharField(max_length=10,choices=STAMP_CHOICES, verbose_name='スタンプ種類')
    verbose_name = 'スタンプ'

    def __str__(self):
        return f'{self.from_user.username} → {self.study_record.title} : {self.stamp_type}'
