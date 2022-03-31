from django import template

#Linhas de código


register = template.Library()

from simplemooc.courses.models import Enrollment

@register.inclusion_tag('courses/templatetags/my_courses.html') #converte essa função em uma tag, recebe uma template como parâmetro para renderizar
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)#retorna as inscricoes do usuário
    context = {
        'enrollments': enrollments
    }
    return context

@register.simple_tag
def load_my_courses(user): #função para atualziar o contexto
    return Enrollment.objects.filter(user=user)