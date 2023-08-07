from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from board.models import Question


def index(request):
    """
    board 목록 출력
    """
    page = request.GET.get('page', '1')
    question_list = Question.objects.all().order_by('-create_date')

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    board 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/question_detail.html', context)
