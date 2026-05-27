from django.db import models


class Student(models.Model):
    name: str = models.CharField(max_length=200, null=False)
    surname: str = models.CharField(max_length=200, null=False)
    email: str = models.EmailField(null=False)

    @property
    def fio(self) -> str:
        return f'{self.surname} {self.name}'

    def __str__(self) -> str:
        return f'{self.surname} {self.name} ({self.email})'

    def __repr__(self) -> str:
        return (
            f'Student(surname="{self.surname}", '
            f'name="{self.name}", '
            f'email="{self.email}")'
        )
