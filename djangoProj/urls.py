# ./djangoProj/urls.py

from django.contrib import admin
from django.urls import path, include
from djangoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),  # 기본 페이지
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),  # 로그인 페이지
    path('signUp/', views.signUp, name='signup'),  # 회원가입 페이지
    path('write/', views.write, name='write'),  # 글 등록 페이지
    path('detail/<int:boardid>/', views.detail, name='detail'),  # 글 상세 페이지
    path('update/<int:boardid>/', views.update, name='update'),
    path('delete/<int:boardid>/', views.delete, name='delete'),
    path('test/', views.test, name = 'test'), # 테스트 페이지
    path('reply/', views.reply, name = 'reply'), # 댓글 페이지
    path('replyUpdate/', views.replyUpdate, name = 'replyUpdate'), # 댓글 수정 페이지
    path('replyDelete/', views.replyDelete, name = 'replyDelete'), # 댓글 삭제 페이지    
]
