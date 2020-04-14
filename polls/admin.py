from django.contrib import admin

# Register your models here.

from .models import Evaluation, Task, Question

admin.site.register(Evaluation)
admin.site.register(Task)
admin.site.register(Question)