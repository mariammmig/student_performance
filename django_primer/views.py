from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import Student, Subject, Score
from .forms import StudentForm, ScoreForm

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sort_by = self.request.GET.get('sort', 'name')
        
        students = Student.objects.prefetch_related('score_set__subject').all()
        
        if sort_by == 'name':
            students = sorted(students, key=lambda s: s.name)
        elif sort_by == 'surname':
            students = sorted(students, key=lambda s: s.surname)
        elif sort_by == 'avg_score':
            students = sorted(students, key=lambda s: s.score_set.aggregate(Avg('value'))['value__avg'] or 0, reverse=True)
        
        subjects = Subject.objects.all()
        
        student_statistics = []
        for student in students:
            scores_dict = {score.subject.name: score.value for score in student.score_set.all()}
            scores_list = [f"{scores_dict.get(subject.name, '-')}" for subject in subjects]
            avg = student.score_set.aggregate(Avg('value'))['value__avg']
            student_statistics.append({
                'student': student,
                'scores': scores_list,
                'avg_score': avg or 0
            })

        all_scores = Score.objects.all()
        if all_scores.exists():
            best_student_id = all_scores.values('student').annotate(avg=Avg('value')).order_by('-avg').first()['student']
            worst_student_id = all_scores.values('student').annotate(avg=Avg('value')).order_by('avg').first()['student']
            best_student = Student.objects.get(id=best_student_id)
            worst_student = Student.objects.get(id=worst_student_id)
            best_avg = all_scores.filter(student=best_student).aggregate(Avg('value'))['value__avg']
            worst_avg = all_scores.filter(student=worst_student).aggregate(Avg('value'))['value__avg']
        else:
            best_student = worst_student = None
            best_avg = worst_avg = 0
        
        context.update({
            'subjects': subjects,
            'student_statistics': student_statistics,
            'best_student': best_student,
            'best_avg': round(best_avg, 2) if best_avg else 0,
            'worst_student': worst_student,
            'worst_avg': round(worst_avg, 2) if worst_avg else 0,
            'current_sort': sort_by,
        })
        return context

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('index')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('index')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('index')

class ScoreCreateView(CreateView):
    model = Score
    form_class = ScoreForm
    template_name = 'score_form.html'
    success_url = reverse_lazy('index')