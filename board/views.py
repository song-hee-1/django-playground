from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/question_detail.html', context)