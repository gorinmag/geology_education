from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    Course, Lesson, StudentProfile, LessonProgress,
    Test, TestQuestion, TestChoiceOption, TestAttempt, TestAnswer,
    Exam, ExamQuestion, ExamChoiceOption, ExamTextAnswer, ExamAttempt, ExamAnswer, RegistrationRequest
)

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Профиль студента'
    fields = ['first_name', 'last_name', 'position']

class UserAdmin(BaseUserAdmin):
    inlines = [StudentProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order_num', 'image_preview', 'video_url', 'video_file']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson_count', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [LessonInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image_preview', 'image')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Количество уроков'

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order_num', 'has_video', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['order_num']
    fieldsets = (
        ('Основная информация', {
            'fields': ('course', 'title', 'content', 'order_num')
        }),
        ('Медиа', {
            'fields': ('image_preview', 'image', 'video_url', 'video_file'),
            'classes': ('wide',),
            'description': 'Загрузите изображение и/или добавьте видео'
        }),
    )
    readonly_fields = ['image_preview']

    def has_video(self, obj):
        return obj.has_video()
    has_video.boolean = True
    has_video.short_description = 'Видео'

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'position', 'user']
    search_fields = ['first_name', 'last_name', 'position']
    list_filter = ['position']
    fields = ['user', 'first_name', 'last_name', 'position']
    readonly_fields = ['user']
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'viewed_at']
    list_filter = ['viewed_at', 'lesson__course']
    search_fields = ['user__username', 'lesson__title']

# ----- Тесты -----
class TestChoiceOptionInline(admin.TabularInline):
    model = TestChoiceOption
    extra = 3

class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1
    show_change_link = True
    fields = ['text', 'points', 'order']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'description']
    inlines = [TestQuestionInline]

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'test', 'points', 'order']
    list_filter = ['test']
    inlines = [TestChoiceOptionInline]

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'started_at', 'completed_at', 'score', 'passed']
    list_filter = ['test', 'passed']
    search_fields = ['user__username']

@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question']
    filter_horizontal = ['selected_options']

# ----- Экзамены -----
class ExamChoiceOptionInline(admin.TabularInline):
    model = ExamChoiceOption
    extra = 2

class ExamTextAnswerInline(admin.TabularInline):
    model = ExamTextAnswer
    extra = 1

class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1
    fields = ['type', 'text', 'points', 'order']
    show_change_link = True

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score', 'allow_retake', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'description']
    inlines = [ExamQuestionInline]

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'exam', 'type', 'points', 'order']
    list_filter = ['exam', 'type']
    inlines = [ExamChoiceOptionInline, ExamTextAnswerInline]

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'started_at', 'completed_at', 'score', 'passed']
    list_filter = ['exam', 'passed']

@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'text_answer']
    filter_horizontal = ['selected_options']

# Добавили запрос регистрации
@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at', 'reviewed_at']
    list_filter = ['status']
    search_fields = ['user__username', 'user__email']
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for reg_request in queryset.filter(status='pending'):
            user = reg_request.user
            user.is_active = True
            user.save()
            reg_request.status = 'approved'
            reg_request.reviewed_at = timezone.now()
            reg_request.save()
        self.message_user(request, f"Одобрено {queryset.count()} заявок.")
    approve_requests.short_description = "Одобрить выбранные заявки"

    def reject_requests(self, request, queryset):
        for reg_request in queryset.filter(status='pending'):
            user = reg_request.user
            # Можно просто удалить пользователя или отметить как отклонённого
            user.delete()  # удаляем пользователя, заявка удалится каскадно
        self.message_user(request, f"Отклонено {queryset.count()} заявок (пользователи удалены).")
    reject_requests.short_description = "Отклонить выбранные заявки (удалить пользователей)"

# Перерегистрируем User с нашей админкой
admin.site.unregister(User)
admin.site.register(User, UserAdmin)