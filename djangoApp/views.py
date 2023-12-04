import json

from django.shortcuts import render, redirect, get_object_or_404
from .form import MemberForm, SignupForm, BoardWriteForm
from .models import Board, Member, Reply
from django.http import JsonResponse

def login(request):
    form = MemberForm()
    return render(request, 'login.html', {'form': form})

def signUp(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def main(request):
    # Board의 모든 데이터를 부른다.
    boardList = Board.objects.all()

    if request.method == 'POST':
        memberName = request.POST.get('memberName')
        password = request.POST.get('password')

        try:
            user = Member.objects.filter(memberName = memberName, password = password).first()

        
            if user is not None:
                request.session['memberid'] = user.id
                return render(request, 'main.html', {'boardList': boardList})
            else:
                return redirect('login')
        except Member.DoesNotExist:
            return redirect('login')
        
    return render(request, 'main.html', {'boardList': boardList})

def write(request):
    if request.method == 'POST':
        form = BoardWriteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
        
    member_id = request.session['memberid']
    member = get_object_or_404(Member, pk=member_id)
    form = BoardWriteForm(initial={'member': member})
    return render(request, 'write.html', {'form': form, 'member': member})

def detail(request, boardid):
    board = get_object_or_404(Board, pk=boardid)

    reply = Reply.objects.filter(board_id = boardid).order_by('-updatedDate')

    try:
        session = request.session['memberid']
        context = {
            'board': board,
            'reply': reply,
            'session': session,
        }
        return render(request, 'detail.html', context)
    except KeyError:
        return redirect('main')

def update(request, boardid):
    if request.method == 'POST':
        board = Board.objects.get(pk=boardid)
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title is not None and board is not None:
            board.title = title
            board.content = content
            board.save()
            return redirect('detail', boardid = boardid)
            # return redirect('detail')
        else:
            return redirect('detail', boardid = boardid)

def delete(request, boardid):
    board = Board.objects.get(pk = boardid)
    print('hello world :: ' + board.title)
    board.delete()
    return redirect('main')

def testPage(request):
    return render(request, 'test.html')

def test(request):
    jsonObject = json.loads(request.body)
    print(jsonObject.get('title'))
    return JsonResponse(jsonObject)

def reply(request):
    jsonObject = json.loads(request.body.decode('utf-8'))

    reply = Reply.objects.create(
    board_id=jsonObject.get('boardId'),
    member_id=jsonObject.get('memberId'),
    content=jsonObject.get('content')
    )

    reply.save()

    context = {
        'name' : reply.member.name,
        'content' : reply.content,
        'createDate' : reply.createdDate,
        'updateDate' : reply.updatedDate
    }
    return JsonResponse(context);

def replyUpdate(request):
    jsonObject = json.loads(request.body)
    reply = Reply.objects.filter(id = jsonObject.get('id'))
    context = {
        'result': 'no'
    }
    if reply is not None:
        reply.update(content = jsonObject.get('content'))
        context = {
            'result' : 'ok'
        }
        return JsonResponse(context);

    return JsonResponse(context);

def replyDelete(request):
    jsonObject = json.loads(request.body)
    context = {
        'result' : 'no'
    }
    reply = Reply.objects.filter(id = jsonObject.get('replyId'))
    if reply is not None:
        reply.delete()
        context = {
            'result' : 'ok'
        }
        return JsonResponse(context);

    return JsonResponse(context);
