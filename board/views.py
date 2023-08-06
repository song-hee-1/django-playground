from django.utils import timezone

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from board.forms import QuestionForm, AnswerForm, CommentForm
from board.models import Question, Answer, Comment


# Create your views here.
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


@login_required(login_url='accounts:login')
def answer_create(request, question_id):
    """
    board 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'board/question_detail.html', context)


@login_required(login_url='accounts:login')
def question_create(request):
    """
    board 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 추가한 속성 author 적용
            question.save()
            question.author = request.user
            return redirect('board:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='accounts:login')
def question_modify(request, question_id):
    """
    질문수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('accounts:detail', question_id>=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='accounts:login')
def question_delete(request, question_id):
    """
    질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')


@login_required(login_url='accounts:login')
def answer_modify(request, answer_id):
    """
    board 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('board:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'board/answer_form.html', context)


@login_required(login_url='accounts:login')
def answer_delete(request, answer_id):
    """
    답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('board:detail', question_id=answer.question.id)

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
            return redirect('board:detail', question_id=question.id)
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
            return redirect('board:detail', question_id=comment.question.id)
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
            return redirect('board:detail', question_id=comment.answer.question.id)
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
            return redirect('board:detail', question_id=comment.answer.question.id)
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
