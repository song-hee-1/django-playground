from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from board.models import Question, Answer


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


@login_required(login_url='accounts:login')
def vote_answer(request, answer_id):
    """
    board 답글 추천 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글을 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('board:detail', question_id=answer.question.id)

