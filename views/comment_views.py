from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from board.forms import CommentForm
from board.models import Question, Answer, Comment


# Create your views here.


@login_required(login_url='accounts:login')
def comment_create_question(request, question_id):
    """
    board 질문댓글등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect(f'{resolve_url("board:detail", question_id=comment.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='accounts:login')
def comment_modify_question(request, comment_id):
    """
    board 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('board:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect(f'{resolve_url("board:detail", question_id=comment.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='accounts:login')
def comment_delete_question(request, comment_id):
    """
    board 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('board:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.question_id)


@login_required(login_url='accounts:login')
def comment_create_answer(request, answer_id):
    """
    board 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect(f'{resolve_url("board:detail", question_id=comment.answer.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='accounts:login')
def comment_modify_answer(request, comment_id):
    """
    board 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('board:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect(f'{resolve_url("board:detail", question_id=comment.answer.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='accounts:login')
def comment_delete_answer(request, comment_id):
    """
    board 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('board:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.answer.question.id)

