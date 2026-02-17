from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import transaction
from .models import (
    Course, Lesson, StudentProfile, LessonProgress,
    Test, TestQuestion, TestChoiceOption, TestAttempt, TestAnswer,
    Exam, ExamQuestion, ExamChoiceOption, ExamTextAnswer, ExamAttempt, ExamAnswer, RegistrationRequest
)
from .forms import StudentRegistrationForm
from django.db.models import Count, Sum, Q
from django.utils import timezone
def index(request):
    courses = Course.objects.all()[:3]
    return render(request, 'courses/index.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons
    })

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    # Получаем предыдущий и следующий уроки по порядку
    lessons = course.lessons.all().order_by('order_num')
    lesson_list = list(lessons)
    try:
        current_index = lesson_list.index(lesson)
    except ValueError:
        current_index = -1

    prev_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson
    })
# Старая функция регистрации
# def register(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             with transaction.atomic():
#                 cd = form.cleaned_data
#                 user = User.objects.create_user(
#                     username=cd['username'],
#                     password=cd['password1'],
#                     email=cd.get('email', '')
#                 )
#                 student_group, _ = Group.objects.get_or_create(name='Студент')
#                 user.groups.add(student_group)
#                 StudentProfile.objects.create(
#                     user=user,
#                     first_name=cd['first_name'],
#                     last_name=cd['last_name'],
#                     position=cd['position']
#                 )
#                 messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
#                 return redirect('courses:login')   # исправлено
#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'courses/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                cd = form.cleaned_data
                # Создаём пользователя, но неактивного
                user = User.objects.create_user(
                    username=cd['username'],
                    password=cd['password1'],
                    email=cd.get('email', ''),
                    is_active=False  # пользователь неактивен до одобрения
                )
                student_group, _ = Group.objects.get_or_create(name='Студент')
                user.groups.add(student_group)
                StudentProfile.objects.create(
                    user=user,
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    position=cd['position']
                )
                # Создаём заявку на регистрацию
                RegistrationRequest.objects.create(user=user)

                messages.success(
                    request,
                    'Регистрационная заявка отправлена! После одобрения администратором вы сможете войти.'
                )
                return redirect('courses:index')
    else:
        form = StudentRegistrationForm()
    return render(request, 'courses/register.html', {'form': form})
# Старая функция
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Для демо-админа (можно убрать в продакшене)
#             if username == 'admin' and password == 'admin' or user.is_superuser:
#                 admin_group, _ = Group.objects.get_or_create(name='Администратор')
#                 user.groups.add(admin_group)
#             messages.success(request, f'Добро пожаловать, {user.username}!')
#             return redirect('courses:course_list')   # исправлено
#         else:
#             messages.error(request, 'Неверное имя пользователя или пароль.')
#     return render(request, 'courses/login.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Для демо-админа (можно убрать в продакшене)
                if username == 'admin' and password == 'admin' or user.is_superuser:
                    admin_group, _ = Group.objects.get_or_create(name='Администратор')
                    user.groups.add(admin_group)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('courses:course_list')
            else:
                messages.error(request, 'Ваша учётная запись ещё не активирована администратором.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'courses/login.html')
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('courses:index')   # исправлено
"""Добавил код"""
@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    # Отмечаем просмотр урока для авторизованного пользователя
    if request.user.is_authenticated:
        LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    # Навигация между уроками (без изменений)
    lessons = course.lessons.all().order_by('order_num')
    lesson_list = list(lessons)
    try:
        current_index = lesson_list.index(lesson)
    except ValueError:
        current_index = -1

    prev_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson
    })

@login_required
def my_courses(request):
    # Получаем все просмотренные уроки пользователя с данными о курсе
    viewed_lessons = LessonProgress.objects.filter(
        user=request.user
    ).select_related('lesson__course').order_by('-viewed_at')

    # Группируем по курсам
    courses_dict = {}
    for progress in viewed_lessons:
        course = progress.lesson.course
        if course.id not in courses_dict:
            courses_dict[course.id] = {
                'course': course,
                'viewed_count': 0,
                'total_lessons': course.lessons.count()
            }
        courses_dict[course.id]['viewed_count'] += 1

    # Вычисляем процент для каждого курса
    courses_list = []
    for data in courses_dict.values():
        data['percent'] = int(data['viewed_count'] / data['total_lessons'] * 100) if data['total_lessons'] > 0 else 0
        courses_list.append(data)

    # Сортируем по дате последнего просмотра (самые свежие сверху)
    courses_list.sort(key=lambda x: x['course'].id, reverse=True)  # можно улучшить сортировку

    return render(request, 'courses/my_courses.html', {'courses_list': courses_list})

# ----- Тесты -----
@login_required
def test_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tests = course.tests.all()
    # Для каждого теста определяем, пройден ли он текущим пользователем
    for test in tests:
        last_attempt = TestAttempt.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
        test.passed = last_attempt.passed if last_attempt else False
        test.attempted = last_attempt is not None
    return render(request, 'courses/test_list.html', {'course': course, 'tests': tests})

@login_required
def test_detail(request, course_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    test = get_object_or_404(Test, id=test_id, course=course)

    # Проверяем, есть ли уже пройденная попытка
    existing_attempt = TestAttempt.objects.filter(user=request.user, test=test, completed_at__isnull=False).first()
    if existing_attempt and not test.allow_retake:  # Если пересдача не разрешена
        return redirect('courses:test_result', course_id=course.id, test_id=test.id, attempt_id=existing_attempt.id)

    if request.method == 'POST':
        # Создаём попытку
        attempt = TestAttempt.objects.create(user=request.user, test=test)
        score = 0
        total_points = test.total_points()
        for question in test.questions.all():
            selected = request.POST.getlist(f'question_{question.id}')
            # Сохраняем ответ
            answer = TestAnswer.objects.create(attempt=attempt, question=question)
            if selected:
                options = TestChoiceOption.objects.filter(id__in=selected)
                answer.selected_options.set(options)
            # Подсчёт баллов
            if answer.is_correct():
                score += question.points
        # Обновляем попытку
        attempt.score = score
        attempt.passed = (score / total_points * 100) >= test.passing_score if total_points else False
        attempt.completed_at = timezone.now()
        attempt.save()
        return redirect('courses:test_result', course_id=course.id, test_id=test.id, attempt_id=attempt.id)

    # GET запрос — показываем форму
    questions = test.questions.all().prefetch_related('options')
    return render(request, 'courses/test_detail.html', {
        'course': course,
        'test': test,
        'questions': questions
    })

@login_required
def test_result(request, course_id, test_id, attempt_id):
    course = get_object_or_404(Course, id=course_id)
    test = get_object_or_404(Test, id=test_id, course=course)
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user, test=test)
    total_points = test.total_points()
    percent = int(attempt.score / total_points * 100) if total_points else 0
    return render(request, 'courses/test_result.html', {
        'course': course,
        'test': test,
        'attempt': attempt,
        'total_points': total_points,
        'percent': percent
    })

# ----- Экзамены -----
@login_required
def exam_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    exams = course.exams.all()
    for exam in exams:
        last_attempt = ExamAttempt.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
        exam.passed = last_attempt.passed if last_attempt else False
        exam.attempted = last_attempt is not None
    return render(request, 'courses/exam_list.html', {'course': course, 'exams': exams})

@login_required
def exam_detail(request, course_id, exam_id):
    course = get_object_or_404(Course, id=course_id)
    exam = get_object_or_404(Exam, id=exam_id, course=course)

    # Проверка на уже пройденную попытку
    existing_attempt = ExamAttempt.objects.filter(user=request.user, exam=exam, completed_at__isnull=False).first()
    if existing_attempt and not exam.allow_retake:
        return redirect('courses:exam_result', course_id=course.id, exam_id=exam.id, attempt_id=existing_attempt.id)

    if request.method == 'POST':
        attempt = ExamAttempt.objects.create(user=request.user, exam=exam)
        score = 0
        total_points = exam.total_points()
        for question in exam.questions.all():
            answer = ExamAnswer.objects.create(attempt=attempt, question=question)
            if question.type == 'choice':
                selected = request.POST.getlist(f'question_{question.id}')
                if selected:
                    options = ExamChoiceOption.objects.filter(id__in=selected)
                    answer.selected_options.set(options)
            else:  # text
                text_answer = request.POST.get(f'question_{question.id}', '').strip()
                answer.text_answer = text_answer
                answer.save()
            score += answer.points_earned()
        attempt.score = score
        attempt.passed = (score / total_points * 100) >= exam.passing_score if total_points else False
        attempt.completed_at = timezone.now()
        attempt.save()
        return redirect('courses:exam_result', course_id=course.id, exam_id=exam.id, attempt_id=attempt.id)

    questions = exam.questions.all().prefetch_related('options', 'text_answers')
    return render(request, 'courses/exam_detail.html', {
        'course': course,
        'exam': exam,
        'questions': questions
    })

@login_required
def exam_result(request, course_id, exam_id, attempt_id):
    course = get_object_or_404(Course, id=course_id)
    exam = get_object_or_404(Exam, id=exam_id, course=course)
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user, exam=exam)
    total_points = exam.total_points()
    percent = int(attempt.score / total_points * 100) if total_points else 0
    return render(request, 'courses/exam_result.html', {
        'course': course,
        'exam': exam,
        'attempt': attempt,
        'total_points': total_points,
        'percent': percent
    })