from django import forms
from .models import Student, Score

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'email']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'Email',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['student', 'subject', 'value']
        labels = {
            'student': 'Студент',
            'subject': 'Предмет',
            'value': 'Оценка',
        }
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '5'}),
        }