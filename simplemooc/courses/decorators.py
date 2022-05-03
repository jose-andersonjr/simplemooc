from getopt import getopt
from webbrowser import get
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from simplemooc.courses.views import Enrollment

from .models import Course, Enrollment

def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        curso = get_object_or_404(Course, slug=slug)
        tem_permissao = request.user.is_staff
        if not tem_permissao:
            try: 
                enrollment = Enrollment.objects.get(
                    user = request.user, curso=curso
                )
            except Enrollment.DoesNotExist:
                message = 'Desculpe, mas você não tem permissão para acessa esta página'
            else:
                if enrollment.is_approved():
                    tem_permissao = True
                else:
                    message = 'A sua inscrição no curso ainda está pendente'
        if not tem_permissao:
            messages.error(request, message)
            return redirect('dashboard')
        request.curso = curso
        return view_func(request, *args, **kwargs)
    return _wrapper

