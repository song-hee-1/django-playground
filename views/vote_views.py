from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from board.models import Question


@login_required(login_url='accounts:login')
def vote_question(request, question_id):
    """
    board 질문 추천 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글을 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('board:detail', question_id=question.id)