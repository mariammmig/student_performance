"""django_primer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import (
    IndexView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    ScoreCreateView,
    StudentSelectEditView,
    StudentSelectDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('student/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('student/select-edit/', StudentSelectEditView.as_view(), name='student_select_edit'),
    path('student/select-delete/', StudentSelectDeleteView.as_view(), name='student_select_delete'),
    path('score/create/', ScoreCreateView.as_view(), name='score_create'),
    path('admin/', admin.site.urls),
]