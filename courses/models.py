from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class StudentProfile(models.Model):
    """
    Профиль студента. Связан один-к-одному с User.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Пользователь'
    )
    # Имя и фамилия дублируются из User для удобства,
    # но можно использовать поля из User напрямую.
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    position = models.CharField('Должность', max_length=200)

    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Course(models.Model):
    title = models.CharField('Название курса', max_length=200)
    description = models.TextField('Описание курса')
    image = models.ImageField(
        'Изображение курса',
        upload_to='courses/',
        blank=True,
        null=True,
        help_text='Загрузите обложку курса (рекомендуемый размер 800x600)'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', args=[str(self.id)])


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    title = models.CharField('Название урока', max_length=200)
    content = models.TextField('Содержание урока')
    image = models.ImageField(
        'Изображение',
        upload_to='lessons/images/',
        blank=True,
        null=True
    )
    video_url = models.URLField(
        'Ссылка на видео',
        blank=True,
        null=True,
        help_text='Например, ссылка на YouTube'
    )
    video_file = models.FileField(
        'Видео файл',
        upload_to='lessons/videos/',
        blank=True,
        null=True,
        help_text='Поддерживаются форматы MP4, WebM, Ogg'
    )
    order_num = models.PositiveIntegerField(
        'Порядковый номер',
        default=0,
        help_text='Чем меньше число, тем раньше показывается урок'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order_num']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def has_video(self):
        """Проверяет наличие видео в уроке"""
        return bool(self.video_url or self.video_file)
"""Добавленный код"""
class LessonProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name='Пользователь'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Урок'
    )
    viewed_at = models.DateTimeField('Дата просмотра', auto_now_add=True)

    class Meta:
        verbose_name = 'Прогресс по уроку'
        verbose_name_plural = 'Прогресс по урокам'
        unique_together = ('user', 'lesson')  # один пользователь – один просмотр на урок

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.viewed_at.strftime('%d.%m.%Y')})"


# Новые модели для тестов и экзаменов

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests', verbose_name='Курс')
    title = models.CharField('Название теста', max_length=200)
    description = models.TextField('Описание', blank=True)
    time_limit = models.PositiveIntegerField('Лимит времени (минут)', default=0, help_text='0 - без ограничения')
    passing_score = models.PositiveIntegerField('Проходной балл (%)', default=70)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def total_points(self):
        return sum(q.points for q in self.questions.all())


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    text = models.TextField('Текст вопроса')
    points = models.PositiveIntegerField('Баллы', default=1)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class TestChoiceOption(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='options', verbose_name='Вопрос')
    text = models.CharField('Текст варианта', max_length=500)
    is_correct = models.BooleanField('Правильный?', default=False)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text[:50]


class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts', verbose_name='Студент')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts', verbose_name='Тест')
    started_at = models.DateTimeField('Начало', auto_now_add=True)
    completed_at = models.DateTimeField('Завершён', null=True, blank=True)
    score = models.PositiveIntegerField('Набрано баллов', default=0)
    passed = models.BooleanField('Пройден?', default=False)

    class Meta:
        verbose_name = 'Попытка теста'
        verbose_name_plural = 'Попытки тестов'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.started_at.strftime('%d.%m.%Y')})"


class TestAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers', verbose_name='Попытка')
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_options = models.ManyToManyField(TestChoiceOption, verbose_name='Выбранные варианты')

    class Meta:
        verbose_name = 'Ответ на тест'
        verbose_name_plural = 'Ответы на тесты'

    def is_correct(self):
        correct_options = set(self.question.options.filter(is_correct=True))
        selected = set(self.selected_options.all())
        return correct_options == selected

    def points_earned(self):
        if self.is_correct():
            return self.question.points
        return 0


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', verbose_name='Курс')
    title = models.CharField('Название экзамена', max_length=200)
    description = models.TextField('Описание', blank=True)
    passing_score = models.PositiveIntegerField('Проходной балл (%)', default=70)
    allow_retake = models.BooleanField('Разрешить пересдачу', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def total_points(self):
        return sum(q.points for q in self.questions.all())


class ExamQuestion(models.Model):
    QUESTION_TYPES = (
        ('choice', 'Выбор ответа'),
        ('text', 'Ручной ввод'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name='Экзамен')
    type = models.CharField('Тип вопроса', max_length=10, choices=QUESTION_TYPES, default='choice')
    text = models.TextField('Текст вопроса')
    points = models.PositiveIntegerField('Баллы', default=1)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Вопрос экзамена'
        verbose_name_plural = 'Вопросы экзамена'
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class ExamChoiceOption(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, related_name='options', verbose_name='Вопрос')
    text = models.CharField('Текст варианта', max_length=500)
    is_correct = models.BooleanField('Правильный?', default=False)

    class Meta:
        verbose_name = 'Вариант ответа (экзамен)'
        verbose_name_plural = 'Варианты ответов (экзамен)'

    def __str__(self):
        return self.text[:50]


class ExamTextAnswer(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, related_name='text_answers', verbose_name='Вопрос')
    correct_answer = models.CharField('Правильный ответ', max_length=500, help_text='Можно указать несколько вариантов через |')

    class Meta:
        verbose_name = 'Эталонный ответ (текст)'
        verbose_name_plural = 'Эталонные ответы (текст)'

    def __str__(self):
        return self.correct_answer[:50]


class ExamAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts', verbose_name='Студент')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts', verbose_name='Экзамен')
    started_at = models.DateTimeField('Начало', auto_now_add=True)
    completed_at = models.DateTimeField('Завершён', null=True, blank=True)
    score = models.PositiveIntegerField('Набрано баллов', default=0)
    passed = models.BooleanField('Пройден?', default=False)

    class Meta:
        verbose_name = 'Попытка экзамена'
        verbose_name_plural = 'Попытки экзаменов'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} ({self.started_at.strftime('%d.%m.%Y')})"


class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers', verbose_name='Попытка')
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_options = models.ManyToManyField(ExamChoiceOption, blank=True, verbose_name='Выбранные варианты')
    text_answer = models.TextField('Текстовый ответ', blank=True)

    class Meta:
        verbose_name = 'Ответ на экзамен'
        verbose_name_plural = 'Ответы на экзамены'

    def points_earned(self):
        if self.question.type == 'choice':
            correct_options = set(self.question.options.filter(is_correct=True))
            selected = set(self.selected_options.all())
            if correct_options == selected:
                return self.question.points
            return 0
        else:  # text
            # Получаем эталонный ответ (может быть несколько через |)
            try:
                correct = self.question.text_answers.first().correct_answer
                # Разделяем по |, убираем пробелы по краям, приводим к нижнему регистру
                correct_variants = [v.strip().lower() for v in correct.split('|')]
                user_answer = self.text_answer.strip().lower()
                if user_answer in correct_variants:
                    return self.question.points
            except AttributeError:
                pass
            return 0
"""Добавление запроса на регистрацию"""
class RegistrationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration_request', verbose_name='Пользователь')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата подачи', auto_now_add=True)
    reviewed_at = models.DateTimeField('Дата рассмотрения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрацию'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"