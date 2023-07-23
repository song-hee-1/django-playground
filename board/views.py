from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from board.models import Question

# Create your views here.
def index(request):
    """
    board 목록 출력
    """
    question_list = Question.objects.all().order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    board 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/question_detail.html', context)


def answer_create(request, question_id):
    """
    board 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'))
    return redirect('board:detail', question_id=question.id)