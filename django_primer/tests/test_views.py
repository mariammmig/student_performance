import pytest
from django.urls import reverse
from django_primer.models import Student, Subject


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'student_statistics' in response.context
    assert 'subjects' in response.context
    assert len(response.context['student_statistics']) > 0


@pytest.mark.django_db
def test_student_create_view(client):
    response = client.post(reverse('student_create'), {
        'name': 'Тестовый',
        'surname': 'Студент',
        'email': 'teststudent@example.com'
    })
    assert response.status_code == 302  # Redirect после успешного создания
    assert Student.objects.filter(email='teststudent@example.com').exists()


@pytest.mark.django_db
def test_student_update_view(client):
    student = Student.objects.first()
    response = client.post(
        reverse('student_update', args=[student.pk]),
        {
            'name': 'Обновлённый',
            'surname': student.surname,
            'email': student.email
        }
    )
    assert response.status_code == 302
    student.refresh_from_db()
    assert student.name == 'Обновлённый'


@pytest.mark.django_db
def test_subject_create_view(client):
    response = client.post(reverse('subject_create'), {
        'name': 'Физика'
    })
    assert response.status_code == 302
    assert Subject.objects.filter(name='Физика').exists()


@pytest.mark.django_db
def test_score_create_view(client):
    student = Student.objects.first()
    subject = Subject.objects.first()

    response = client.post(reverse('score_create'), {
        'student': student.id,
        'subject': subject.id,
        'value': 4.2
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_student_create_invalid_data(client):
    response = client.post(reverse('student_create'), {
        'name': '',
        'surname': 'Тестов',
        'email': 'invalid-email'
    })
    assert response.status_code == 200


@pytest.mark.django_db
class TestStudentsSelectViews:
    def test_student_select_edit_get(self, client):
        response = client.get(reverse('student_select_edit'))
        assert response.status_code == 200
        assert 'students' in response.context
        assert (
            'delete_mode' not in response.context
            or not response.context.get('delete_mode')
        )

    def test_student_select_delete_get(self, client):
        response = client.get(reverse('student_select_delete'))
        assert response.status_code == 200
        assert response.context['delete_mode'] is True


@pytest.mark.django_db
def test_score_create_get(client):
    response = client.get(reverse('score_create'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_score_select_delete_get(client):
    response = client.get(reverse('score_select_delete'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_subject_select_edit_get(client):
    response = client.get(reverse('subject_select_edit'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_subject_select_delete_get(client):
    response = client.get(reverse('subject_select_delete'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_select_edit_get(client):
    response = client.get(reverse('student_select_edit'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_select_delete_get(client):
    response = client.get(reverse('student_select_delete'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_score_select_edit_get(client):
    response = client.get(reverse('score_select_edit'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_select_edit_post(client):
    student = Student.objects.first()
    response = client.post(reverse('student_select_edit'), {
        'student_id': student.id
    })
    assert response.status_code == 302
    assert response.url == reverse('student_update', args=[student.id])


@pytest.mark.django_db
def test_student_select_delete_post(client):
    student = Student.objects.create(
        name='ДляУдаления',
        surname='Тестовый',
        email='delete@example.com'
    )
    response = client.post(reverse('student_select_delete'), {
        'student_id': student.id
    })
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert not Student.objects.filter(id=student.id).exists()
