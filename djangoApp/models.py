from django.db import models

# Create your models here.

#회원 정보
class Member(models.Model):
    memberName = models.CharField(max_length=10)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    createdDate = models.DateTimeField(auto_now_add = True)
    updatedDate = models.DateTimeField(auto_now=True)

#게시판
class Board(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=255, null = False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add = True)
    updatedDate = models.DateTimeField(auto_now=True)

#댓글
class Reply(models.Model):
    content = models.CharField(max_length=255, null = True)

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)