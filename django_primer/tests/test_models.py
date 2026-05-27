import pytest
from django_primer.models import Student, Subject, Score


@pytest.mark.django_db
class TestStudentModel:
    def test_create_student(self):
        student = Student.objects.create(
            name="Тестовый",
            surname="Пользователь",
            email="test@example.com"
        )
        assert student.pk is not None
        assert student.fio == "Пользователь Тестовый"

    def test_student_str(self):
        student = Student.objects.create(
            name="Иван", surname="Иванов", email="ivan@example.com"
        )
        assert str(student) == "Иванов Иван (ivan@example.com)"


@pytest.mark.django_db
class TestScoreModel:
    def test_score_creation(self):
        student = Student.objects.first()
        subject = Subject.objects.first()

        score = Score.objects.create(
            student=student,
            subject=subject,
            value=4.7
        )
        assert score.value == 4.7
        assert score.student == student
        assert score.subject == subject


@pytest.mark.django_db
def test_subject_creation():
    subject = Subject.objects.create(name="Математика")
    assert subject.name == "Математика"
    assert str(subject) == "Математика"


@pytest.mark.django_db
def test_score_with_student_and_subject():
    student = Student.objects.first()
    subject = Subject.objects.first()

    score = Score.objects.create(student=student, subject=subject, value=3.8)
    assert score.student == student
    assert score.subject == subject
    assert score.value == 3.8
