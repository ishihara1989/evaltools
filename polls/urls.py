from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('evaluation/<int:evaluation_id>', views.evaluation, name='evaluation'),
    path('start/<int:evaluation_id>', views.start, name='start'),
    path('total/<int:evaluation_id>', views.total, name='total'),
    path('question/<str:task_id>/<int:question_order>', views.question, name='question'),
    path('submit/<int:question_id>', views.submit, name='submit'),
    path('wave/<int:question_id>.wav', views.wave, name='wave'),
    path('result/<str:task_id>', views.result, name='result')
]
