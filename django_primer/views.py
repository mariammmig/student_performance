from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Avg
from django.shortcuts import redirect, get_object_or_404

from .models import Student, Subject, Score
from .forms import StudentForm, ScoreForm


class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sort_by = self.request.GET.get('sort', 'name')
        
        students = list(Student.objects.prefetch_related('score_set__subject').all())
        
        if sort_by == 'name':
            students.sort(key=lambda s: (s.name.lower(), s.surname.lower()))
        
        elif sort_by == 'surname':
            students.sort(key=lambda s: (s.surname.lower(), s.name.lower()))
        
        elif sort_by == 'avg_score':
            def get_avg(student):
                scores = student.score_set.all()
                if scores:
                    return sum(s.value for s in scores) / len(scores)
                return 0
            students.sort(key=get_avg, reverse=True)
        
        subjects = Subject.objects.all()
        
        student_statistics = []
        for student in students:
            scores_dict = {score.subject.name: score.value for score in student.score_set.all()}
            scores_list = []
            for subject in subjects:
                value = scores_dict.get(subject.name, 0)
                scores_list.append(f"{value:.1f}" if value > 0 else "-")
        
            score_values = [score.value for score in student.score_set.all()]
            avg_score = sum(score_values) / len(score_values) if score_values else 0
            
            student_statistics.append({
                'student': student,
                'scores': scores_list,
                'avg_score': round(avg_score, 2)
            })
        
        if student_statistics:
            best = max(student_statistics, key=lambda x: x['avg_score'])
            worst = min(student_statistics, key=lambda x: x['avg_score'])
            best_student = best['student']
            worst_student = worst['student']
            best_avg = best['avg_score']
            worst_avg = worst['avg_score']
        else:
            best_student = worst_student = None
            best_avg = worst_avg = 0
        
        context.update({
            'subjects': subjects,
            'student_statistics': student_statistics,
            'best_student': best_student,
            'best_avg': best_avg,
            'worst_student': worst_student,
            'worst_avg': worst_avg,
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
    template_name = 'student_delete.html'
    success_url = reverse_lazy('index')


class ScoreCreateView(CreateView):
    model = Score
    form_class = ScoreForm
    template_name = 'score_form.html'
    success_url = reverse_lazy('index')


class ScoreUpdateView(UpdateView):
    model = Score
    form_class = ScoreForm
    template_name = 'score_form.html'
    success_url = reverse_lazy('index')


class ScoreSelectEditView(TemplateView):
    template_name = 'score_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scores'] = Score.objects.select_related('student', 'subject').all().order_by('student__surname', 'student__name')
        return context

    def post(self, request):
        score_id = request.POST.get('score_id')
        if score_id:
            return redirect('score_update', pk=score_id)
        return redirect('index')


class ScoreSelectDeleteView(TemplateView):
    template_name = 'score_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scores'] = Score.objects.select_related('student', 'subject').all().order_by('student__surname', 'student__name')
        context['delete_mode'] = True
        return context

    def post(self, request):
        score_id = request.POST.get('score_id')
        if score_id:
            score = get_object_or_404(Score, pk=score_id)
            score.delete()
        return redirect('index')
    
class StudentSelectEditView(TemplateView):
    template_name = 'student_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all().order_by('surname', 'name')
        return context

    def post(self, request):
        student_id = request.POST.get('student_id')
        if student_id:
            return redirect('student_update', pk=student_id)
        return redirect('index')


class StudentSelectDeleteView(TemplateView):
    template_name = 'student_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all().order_by('surname', 'name')
        context['delete_mode'] = True
        return context

    def post(self, request):
        student_id = request.POST.get('student_id')
        if student_id:
            student = get_object_or_404(Student, pk=student_id)
            student.delete()
        return redirect('index')
    