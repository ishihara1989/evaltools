from django.db import models
from django.core.validators import MinValueValidator
import uuid

# Create your models here.

class Evaluation(models.Model):
    method_a = models.CharField(max_length=256)
    method_b = models.CharField(max_length=256)
    n_questions = models.PositiveSmallIntegerField(null=False, default=5, validators=[MinValueValidator(1)])
    n_data = models.PositiveSmallIntegerField(null=False, default=10, validators=[MinValueValidator(1)])

    def number_of_questions(self):
        return self.n_questions*2

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

class Question(models.Model):
    order = models.PositiveSmallIntegerField(null=False, default=127, validators=[MinValueValidator(1)])
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    src_speaker = models.CharField(max_length=256)
    tgt_speaker = models.CharField(max_length=256)
    utterance = models.CharField(max_length=256)
    is_inverted = models.BooleanField(default=False)
    is_former_better = models.NullBooleanField()
