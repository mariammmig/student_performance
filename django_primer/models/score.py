from django.db import models

from .student import Student
from .subject import Subject


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.FloatField(blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.student.fio}: {self.subject} -> {self.value:.2f}'

    def __repr__(self) -> str:
        return (
            f'Score(student="{self.student}", '
            f'subject="{self.subject}", '
            f'value={self.value})'
        )
