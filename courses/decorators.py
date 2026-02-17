"""
Декораторы для проверки прав доступа.

Декораторы - это функции, которые "оборачивают" другие функции
и добавляют дополнительную логику до или после выполнения.
"""

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Декоратор, требующий прав администратора для доступа к представлению.

    Использование:
    @admin_required
    def some_view(request):
        ...
    """

    @wraps(view_func)  # Сохраняет имя и docstring оригинальной функции
    def _wrapped_view(request, *args, **kwargs):
        # Проверяем, авторизован ли пользователь и является ли администратором
        if not request.user.is_authenticated:
            messages.error(request, 'Для доступа к этой странице необходимо войти.')
            return redirect('login')

        # Проверка на администратора
        is_admin = (
                request.user.is_superuser or
                request.user.groups.filter(name='Администратор').exists()
        )

        if not is_admin:
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('index')

        # Если все проверки пройдены, вызываем оригинальную функцию
        return view_func(request, *args, **kwargs)

    return _wrapped_view