def user_info(request):
    context = {
        'user': request.user,
    }
    if request.user.is_authenticated:
        context['is_admin'] = (
            request.user.is_superuser or
            request.user.groups.filter(name='Администратор').exists()
        )
        context['is_student'] = request.user.groups.filter(name='Студент').exists()
        if hasattr(request.user, 'student_profile'):
            context['student_profile'] = request.user.student_profile
    return context