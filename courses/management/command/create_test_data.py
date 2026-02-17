"""
Кастомная команда Django для создания тестовых данных.

Использование:
python manage.py create_test_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from courses.models import Course, Lesson, StudentProfile


class Command(BaseCommand):
    """
    Команда для заполнения базы тестовыми данными.
    """

    help = 'Создает тестовые данные для курсов геологии'

    def handle(self, *args, **options):
        """
        Основной метод команды.
        """
        self.stdout.write(self.style.SUCCESS('Начинаем создание тестовых данных...'))

        # Создаем группы
        admin_group, _ = Group.objects.get_or_create(name='Администратор')
        student_group, _ = Group.objects.get_or_create(name='Студент')

        # Создаем тестового студента
        if not User.objects.filter(username='student').exists():
            user = User.objects.create_user(
                username='student',
                password='student123',
                email='student@example.com'
            )
            user.groups.add(student_group)

            StudentProfile.objects.create(
                user=user,
                first_name='Иван',
                last_name='Петров',
                position='Геолог-практикант'
            )
            self.stdout.write(self.style.SUCCESS('Создан тестовый студент'))

        # Создаем тестовый курс
        if not Course.objects.filter(title='Введение в геологию').exists():
            course = Course.objects.create(
                title='Введение в геологию',
                description='Базовый курс для начинающих геологов. Вы узнаете о составе Земли, минералах, горных породах и основных геологических процессах.'
            )

            # Создаем уроки
            lessons = [
                {
                    'title': 'Что такое геология?',
                    'content': 'Геология - это наука о Земле, её составе, строении и истории развития. В этом уроке мы рассмотрим основные направления геологии и её значение для человечества.',
                    'order': 1
                },
                {
                    'title': 'Минералы и их свойства',
                    'content': 'Минералы - это природные тела с определённым химическим составом и кристаллической структурой. Изучим основные свойства минералов: твёрдость, спайность, блеск, цвет.',
                    'order': 2
                },
                {
                    'title': 'Горные породы',
                    'content': 'Горные породы состоят из минералов. Различают магматические, осадочные и метаморфические породы. Рассмотрим их происхождение и примеры.',
                    'order': 3
                },
            ]

            for lesson_data in lessons:
                Lesson.objects.create(course=course, **lesson_data)

            self.stdout.write(self.style.SUCCESS('Создан тестовый курс с уроками'))

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))