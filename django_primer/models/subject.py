from django.db import models


class Subject(models.Model):
    name: str = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Subject(name="{self.name}")'
