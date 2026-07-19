from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChapterProgress, CurriculumChapter, CurriculumItem, TraineeProfile

User = get_user_model()


class CurriculumItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumItem
        fields = ['id', 'chapter', 'item_number', 'title', 'order']
        read_only_fields = ['chapter']


class CurriculumChapterSerializer(serializers.ModelSerializer):
    """カリキュラム一覧・新規追加・編集用（要件3-3）"""
    items = CurriculumItemSerializer(many=True, required=False)

    class Meta:
        model = CurriculumChapter
        fields = ['id', 'chapter_number', 'title', 'estimated_days', 'order', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        chapter = CurriculumChapter.objects.create(**validated_data)
        for item_data in items_data:
            CurriculumItem.objects.create(chapter=chapter, **item_data)
        return chapter

    def update(self, instance, validated_data):
        # 小項目(items)の増減は別途Item用エンドポイントで扱うため、章自体の項目のみ更新する
        validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CurriculumItemOptionSerializer(serializers.ModelSerializer):
    """受講生側の小項目選択UI用"""

    class Meta:
        model = CurriculumItem
        fields = ['id', 'item_number', 'title', 'order']


class CurriculumChapterOptionSerializer(serializers.ModelSerializer):
    """受講生側の章選択UI用（要件4-3・4-4）。全認証済みユーザーが閲覧可能。
    選択した章に対応する小項目も併せて選べるよう、items をネストして返す。
    """
    items = CurriculumItemOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CurriculumChapter
        fields = ['id', 'chapter_number', 'title', 'order', 'items']


class ChapterReorderSerializer(serializers.Serializer):
    """章の並び替え（ドラッグ&ドロップ/上下ボタン）要件3-3-a"""
    id = serializers.IntegerField()
    order = serializers.IntegerField()


class ChapterProgressSerializer(serializers.ModelSerializer):
    chapter_number = serializers.CharField(source='chapter.chapter_number', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)

    class Meta:
        model = ChapterProgress
        fields = [
            'id', 'chapter', 'chapter_number', 'chapter_title',
            'is_completed', 'completed_at', 'total_minutes',
        ]


class TraineeListSerializer(serializers.ModelSerializer):
    """受講生一覧表示用（要件3-1-a）"""
    name = serializers.CharField(source='user.username', read_only=True)
    mentor_name = serializers.SerializerMethodField()
    current_chapter = serializers.SerializerMethodField()
    is_delayed = serializers.SerializerMethodField()

    class Meta:
        model = TraineeProfile
        fields = [
            'id', 'name', 'status', 'mentor_name', 'start_date',
            'expected_end_date', 'current_chapter', 'is_delayed',
        ]

    def get_mentor_name(self, obj):
        return obj.mentor.username if obj.mentor else None

    def get_current_chapter(self, obj):
        chapter = obj.get_current_chapter()
        if not chapter:
            return None
        return {
            'id': chapter.id,
            'chapter_number': chapter.chapter_number,
            'title': chapter.title,
        }

    def get_is_delayed(self, obj):
        return obj.is_delayed()


class TraineeDetailSerializer(TraineeListSerializer):
    """進捗管理・受講生詳細画面用（要件3-1-c）"""
    chapter_progresses = ChapterProgressSerializer(many=True, read_only=True)
    reflections = serializers.SerializerMethodField()

    class Meta(TraineeListSerializer.Meta):
        fields = TraineeListSerializer.Meta.fields + ['chapter_progresses', 'reflections']

    def get_reflections(self, obj):
        # 振り返り記録（疑問点・苦労・できたこと・解決策・理解度）を講師が閲覧できるようにする
        from study.models import StudyRecord

        records = (
            StudyRecord.objects.filter(user=obj.user, category__name='curriculum')
            .select_related('chapter', 'item')
            .order_by('-study_date')
        )
        return [
            {
                'chapter': record.chapter.chapter_number if record.chapter else None,
                'chapter_title': record.chapter.title if record.chapter else None,
                'item': record.item.item_number if record.item else None,
                'item_title': record.item.title if record.item else None,
                'study_date': record.study_date,
                'questions': record.questions,
                'struggles': record.struggles,
                'achievements': record.achievements,
                'solutions': record.solutions,
                'understanding': record.understanding,
            }
            for record in records
        ]


class TraineeRegisterSerializer(serializers.Serializer):
    """受講生登録（要件3-1-b）：Monster Study Tracker登録済みユーザーからtraineeロールを付与"""
    user_id = serializers.IntegerField()
    mentor_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('ユーザーが見つかりません')
        if hasattr(user, 'trainee_profile'):
            raise serializers.ValidationError('既に受講生として登録されています')
        if user.role in ('instructor', 'admin'):
            raise serializers.ValidationError('講師・管理者ロールを持つユーザーは受講生として登録できません')
        return value

    def validate_mentor_id(self, value):
        if not value:
            return value
        mentor = User.objects.filter(id=value).first()
        if not mentor:
            raise serializers.ValidationError('担当メンバーが見つかりません')
        if mentor.role not in ('instructor', 'admin'):
            raise serializers.ValidationError('担当メンバーは講師または管理者ロールのユーザーのみ指定できます')
        return value

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        user.role = 'trainee'
        user.save(update_fields=['role'])

        mentor = None
        if validated_data.get('mentor_id'):
            mentor = User.objects.filter(id=validated_data['mentor_id']).first()

        # 登録直後のステータスは「未受講」で固定（要件3-1-b）
        return TraineeProfile.objects.create(user=user, mentor=mentor)


class TraineeStatusUpdateSerializer(serializers.Serializer):
    """受講生ステータス変更（未受講→受講中→完了）要件3-1-a"""
    status = serializers.ChoiceField(choices=TraineeProfile.STATUS_CHOICES)
    start_date = serializers.DateField(required=False)

    def validate(self, attrs):
        target_status = attrs['status']
        if target_status == TraineeProfile.STATUS_IN_PROGRESS:
            if not attrs.get('start_date') and not self.instance.start_date:
                raise serializers.ValidationError(
                    {'start_date': '「受講中」に変更する場合は学習開始日の入力が必要です'}
                )
        return attrs

    def update(self, instance, validated_data):
        new_status = validated_data['status']
        if new_status == TraineeProfile.STATUS_IN_PROGRESS:
            if validated_data.get('start_date'):
                instance.start_date = validated_data['start_date']
            # 完了予定日は全13章の想定日数合計(90日)から自動算出（要件3-1-b）
            instance.expected_end_date = instance.calculate_expected_end_date()
        instance.status = new_status
        instance.save()
        return instance


class InstructorRegisterSerializer(serializers.Serializer):
    """講師ロール付与（adminアカウントのみ実行可、要件3-1-b・v3確定No.3）"""
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('ユーザーが見つかりません')
        if hasattr(user, 'trainee_profile'):
            raise serializers.ValidationError('既に受講生として登録されているユーザーは講師にできません')
        return value

    def save(self, **kwargs):
        user = User.objects.get(id=self.validated_data['user_id'])
        user.role = 'instructor'
        user.save(update_fields=['role'])
        return user


class UserCandidateSerializer(serializers.ModelSerializer):
    """受講生登録画面に表示する、アプリ登録済みユーザー一覧用（要件3-1-b）"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
