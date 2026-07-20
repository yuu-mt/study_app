from django.contrib import admin

from .models import ChapterProgress, CurriculumChapter, CurriculumItem, TraineeProfile


class CurriculumItemInline(admin.TabularInline):
    model = CurriculumItem
    extra = 0


@admin.register(CurriculumChapter)
class CurriculumChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_number', 'title', 'estimated_days', 'order')
    ordering = ('order',)
    inlines = [CurriculumItemInline]


@admin.register(TraineeProfile)
class TraineeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'mentor', 'start_date', 'expected_end_date')
    list_filter = ('status',)


@admin.register(ChapterProgress)
class ChapterProgressAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'chapter', 'is_completed', 'completed_at', 'total_minutes')
    list_filter = ('is_completed', 'chapter')
