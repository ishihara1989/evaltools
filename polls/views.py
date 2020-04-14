import pathlib
from io import BytesIO
from random import randint
import numpy as np
import scipy.io.wavfile as wavfile

from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.template import loader

from .models import Evaluation, Task, Question

eval_root = pathlib.Path('/home/ubuntu/nn/data/eval')

def index(request):
    eval_list = Evaluation.objects.all()
    context = {
        'eval_list': eval_list
    }
    return render(request, 'polls/index.html', context)

def evaluation(request, evaluation_id):
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    context = {
        'evaluation': evaluation
    }
    return render(request, 'polls/evaluation.html', context)

def random_comb(n):
    i = randint(1, n)
    j = randint(1, n-1)
    if j>=i:
        j += 1
    c = randint(0, 1)
    i = f"jvs{i+90:03}"
    j = f"jvs{j+90:03}"
    if c==0:
        return (i, j)
    else:
        return (j, i)

def start(request, evaluation_id):
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    tgt_list = np.random.permutation(evaluation.n_data)[:evaluation.number_of_questions()//2]
    tgt_list = [(f"{i+91:03}.wav", *random_comb(10), False) for i in tgt_list]
    tgt_list2 = [(*t, True) for t in tgt_list]
    c = randint(0, 1)
    if c==0:
        tgt_list = tgt_list + tgt_list2
    else:
        tgt_list = tgt_list2 + tgt_list
    task = evaluation.task_set.create()
    for i in range(0, evaluation.number_of_questions()):
        q = task.question_set.create(
            order=i+1,
            src_speaker=tgt_list[i][1],
            tgt_speaker=tgt_list[i][2],
            utterance=tgt_list[i][0],
            is_inverted=tgt_list[i][3])

    return redirect('polls:question', task_id=task.id, question_order=1)

def question(request, task_id, question_order):
    question = Question.objects.filter(task__pk=task_id, order=question_order)[0]
    context = {
        'question': question
    }
    return render(request, 'polls/question.html', context)

def wave(request, question_id):
    question = Question.objects.get(pk=question_id)
    src_speaker = question.src_speaker
    tgt_speaker = question.tgt_speaker
    utterance = question.utterance

    method_A = question.task.evaluation.method_a
    method_B = question.task.evaluation.method_b
    if question.is_inverted:
        t = method_A
        method_A = method_B
        method_B = t

    ref_path = eval_root/method_A/tgt_speaker/'ref.wav'
    wave_A_path = eval_root/method_A/tgt_speaker/src_speaker/utterance
    wave_B_path = eval_root/method_B/tgt_speaker/src_speaker/utterance

    sr, ref = wavfile.read(ref_path)
    _, waveA = wavfile.read(wave_A_path)
    _, waveB = wavfile.read(wave_B_path)
    wave = np.hstack((ref, waveA, waveB))
    byte = BytesIO()
    wavfile.write(byte, sr, wave)
    byte.seek(0)

    return FileResponse(byte, filename="wave.wav")


def submit(request, question_id):
    is_a = True if request.POST['is_a'] == 'A' else False if request.POST['is_a'] == 'B' else None
    question = Question.objects.get(pk=question_id)
    question.is_former_better = is_a ^ question.is_inverted
    question.save()
    task = question.task
    evaluation = task.evaluation
    if question.order == evaluation.number_of_questions():
        return redirect('polls:result', task_id=task.id)
    else:
        return redirect('polls:question', task_id=task.id, question_order=question.order+1)

def result(request, task_id):
    task = Task.objects.get(pk=task_id)
    questions = task.question_set.all()
    valid = all([q.is_former_better is not None for q in questions])
    first_q = None
    for q in questions:
        if q.is_former_better is None:
            first_q = q
            break
    context = {
        'questions': questions,
        'valid': first_q is None,
        'first_q': first_q
    }
    return render(request, 'polls/result.html', context)