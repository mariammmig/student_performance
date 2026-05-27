import pytest
from django.urls import reverse
from django_primer.models import Student, Subject, Score


@pytest.mark.django_db
def test_get_students():
    assert Student.objects.count() == 3


@pytest.mark.django_db
def test_student_fio_property():
    student = Student.objects.first()
    assert student.fio == f"{student.surname} {student.name}"


@pytest.mark.django_db
def test_subject_str():
    subject = Subject.objects.first()
    assert str(subject) == subject.name


@pytest.mark.django_db
def test_score_str():
    score = Score.objects.first()
    assert str(score) == (
        f"{score.student.fio}: {score.subject} -> {score.value:.2f}"
    )


@pytest.mark.django_db
def test_index_view_status_code(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'student_statistics' in response.context
    assert 'subjects' in response.context
