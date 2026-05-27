import pytest
from django_primer.forms import StudentForm, ScoreForm, SubjectForm


@pytest.mark.django_db
def test_student_form_valid():
    form = StudentForm(data={
        'name': 'Алексей',
        'surname': 'Иванов',
        'email': 'alex@example.com'
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_student_form_invalid():
    form = StudentForm(data={
        'name': '',
        'surname': 'Иванов',
        'email': 'bad-email'
    })
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'email' in form.errors


@pytest.mark.django_db
def test_subject_form_valid():
    form = SubjectForm(data={'name': 'Математика'})
    assert form.is_valid()


@pytest.mark.django_db
def test_score_form_valid():
    form = ScoreForm(data={
        'student': 1,
        'subject': 1,
        'value': 4.7
    })
    assert form.is_valid()
