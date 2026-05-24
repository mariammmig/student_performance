from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200, null=False)
    surname = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)

    @property
    def fio(self):
        return f'{self.surname} {self.name}' 

    def __str__(self):
        return f'{self.surname} {self.name} ({self.email})'

    def __repr__(self):
        return f'Student(surname="{self.surname}", name="{self.name}", email="{self.email}")'