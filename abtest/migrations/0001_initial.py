# Generated by Django 3.0.5 on 2020-04-17 15:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_a', models.CharField(max_length=256)),
                ('method_b', models.CharField(max_length=256)),
                ('n_questions', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)])),
                ('n_data', models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abtest.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=127, validators=[django.core.validators.MinValueValidator(1)])),
                ('src_speaker', models.CharField(max_length=256)),
                ('tgt_speaker', models.CharField(max_length=256)),
                ('utterance', models.CharField(max_length=256)),
                ('is_inverted', models.BooleanField(default=False)),
                ('is_former_better', models.NullBooleanField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abtest.Task')),
            ],
        ),
    ]