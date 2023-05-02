from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Course, Lecture, Test, Test_Attempt, Test_Mark
from informing_app.models import Course_Announce
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from users.models import Teacher_Profile, Student_Profile, Study_Group
from .decorators import check_course_existence, course_access, check_test_existence
from .forms import QuizShowForm, QuizUpdateForm, QuizPublishForm, QuizAttemptCheckForm, QuizAttemptDeniedForm
from django.http import HttpRequest
from django.shortcuts import redirect
import json
from . import test_methods
from . import file_methods
import os
from django.core.files import File
from django.db.models import Sum

class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    template_name = 'educational/lecture_create.html'
    fields = ['file']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        if Course.objects.get(pk=kwargs['id']).author != request.user.teacher_profile:
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['id']
            return super(LectureCreateView, self).dispatch(request)
    
    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')
    
class LectureDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecture
    template_name = 'educational/lecture_delete.html'

    def get_success_url(self):
        return reverse('main')

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'educational/course_create.html'
    fields = ['title', 'groups', 'description']

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            return super(CourseCreateView, self).dispatch(request)

    def form_valid(self, form):
        form.instance.author = self.request.user.teacher_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')    

@login_required(login_url='/login/')
@check_course_existence
@course_access
def get_course(request, id):
    f_course = Course.objects.filter(pk=id).first()
    return render(request, 'educational/course.html', 
                  {'course': f_course, 
                   'lectures': Lecture.objects.filter(course=f_course).all(),
                   'announces': Course_Announce.objects.filter(course=f_course).order_by('-publish_date'),
                   'tests': Test.objects.filter(course=f_course).all()})

@login_required(login_url='/login/')
@check_test_existence
def get_test(request, id):
    test = Test.objects.get(pk=id)
    with open(test.filepath, encoding='utf-8') as json_file:
        test_f = json.load(json_file)
    
    if hasattr(request.user, 'student_profile'):
        if test.status == "PROCESS" or test.status == "CLOSED":
            return HttpResponse(status=400)
        ta_check = [at[0] for at in Test_Attempt.objects.filter(student=request.user.student_profile).filter(test=test).values_list('status')]
        if 'CHECK' in ta_check or 'ACCESS' in ta_check:
            return redirect('course-view', id=test.course.pk)
        form = QuizShowForm(questions=test_f['questions'])
        temp = 'educational/test.html'
        context = {'form': form}
    elif hasattr(request.user, 'teacher_profile'):
        if test.status == "PROCESS":
            publish_check = QuizPublishForm()
            form = QuizUpdateForm(instance=test)
            temp = 'educational/test_update.html'
            context = {'form': form, 'publish': publish_check,
                       'questions': test_f['questions'], 'id': test.pk}
        else:
            context = {'students':[], 'test':test}
            temp = 'educational/test_list.html'
            students = Student_Profile.objects.filter(group__in=test.course.groups.all())
            for st in students: context['students'].append([f'{st.first_name} {st.last_name}', Test_Attempt.objects.filter(student=st).filter(test=test).order_by('publish_date')])

    if request.method == 'POST':
        if 'quiz_show' in request.POST:
            res = dict(request.POST)
            del res['csrfmiddlewaretoken']
            del res['quiz_show']
            test_list = test_methods.test_dict_to_list(test_f['questions'])
            total_points = sum([question[2] for question in test_list])
            solution = test_methods.generate_solution_file(test_list, test_methods.solution_dict_to_list(res))
            form.save(solution, request.user, test)
            res_points = sum([solution[ans][1] for ans in solution])
            return render(request, 'educational/test_res.html', {'res': res_points, 'total': total_points})
        elif 'publish_st' in request.POST:
            test.status = 'DONE'
            test.save()
            return redirect('course-view', id=test.course.pk)
        else:
            edit_form = QuizUpdateForm(request.POST, instance=test)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('test', id=id)
    return render(request, temp, context)

@login_required(login_url='/login/')
def get_lecture(request, id):
    lecture = Lecture.objects.get(pk=id)
    resp = HttpResponse(lecture.file, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{ lecture.filename }"'
    return resp

@login_required(login_url='/login/')
def get_test_attempt(request, id):
    test_attempt = Test_Attempt.objects.get(pk=id)
    test = test_attempt.test
    with open(test_attempt.filepath, 'r', encoding='cp1251') as json_file: # ошибка на стороне записи попытки, исправить
        test_at = json.load(json_file)
    with open(test.filepath, encoding='utf-8') as json_file:
        test_f = json.load(json_file)
    if test_attempt.status == 'CHECK': 
        temp = 'educational/test_attempt_check.html'
        context={'form': QuizAttemptCheckForm(test_at),
                 'denied': QuizAttemptDeniedForm(), 
                 'ats': test_methods.get_test_attempt_list(test_at, test_f['questions'])}
    else: 
        temp = 'educational/test_attempt.html'
        context={'ats': test_methods.get_test_attempt_list(test_at, test_f['questions'])}

    if request.method == 'POST':
        if 'denied_st' in request.POST:
            test_attempt.status = 'DENIED'
            test_attempt.save()
            return redirect('test', id=test.pk)
        else:
            res = [int(value[0]) for key, value in dict(request.POST).items() if key != 'csrfmiddlewaretoken']
            interm_file_path = os.path.join(file_methods.PATH, 'intermediate_content', 
                              f'{file_methods.get_transliteration(test.name)}.json')
            f = open(interm_file_path, 'a+', encoding='utf-8')
            res_str = json.dumps(test_methods.set_test_attempt(test_at, res), indent = 2, ensure_ascii=False)
            f.write(res_str)
            test_attempt.file.delete()
            test_attempt.file = File(f)
            test_attempt.status = 'ACCESS'
            test_attempt.save(update_fields=['file', 'status'])
            f.close()
            os.remove(interm_file_path)
            test_mark = Test_Mark(test=test, test_attempt=test_attempt, 
                                  student=test_attempt.student, 
                                  points=test_methods.get_test_attempt_points(test_at),
                                  max_points=test_methods.get_test_points(test_f))
            test_mark.save()
            return redirect('test', id=test.pk)

    return render(request, temp, context)

@login_required(login_url='/login/')
def close_test(request, id):
    test = Test.objects.get(pk=id)
    with open(test.filepath, encoding='utf-8') as json_file:
        test_f = json.load(json_file)
    if request.method == 'POST':
        res=[]
        for st in Student_Profile.objects.filter(group__in=test.course.groups.all()): 
            if not Test_Attempt.objects.filter(student=st).filter(test=test):
                test_mark = Test_Mark(test=test, student=st, 
                                      points=0, max_points=test_methods.get_test_points(test_f))
                test_mark.save()
            else:
                match Test_Attempt.objects.filter(student=st).filter(test=test).order_by('publish_date').last().status:
                    case 'ACCESS':
                        continue
                    case 'DENIED':
                        test_mark = Test_Mark(test=test, student=st, 
                                      points=0, max_points=test_methods.get_test_points(test_f))
                        test_mark.save()
                    case 'CHECK':
                        ta = Test_Attempt.objects.filter(student=st).filter(test=test).order_by('publish_date').last()
                        with open(ta.filepath, 'r', encoding='cp1251') as json_file: # ошибка на стороне записи попытки, исправить
                            test_at = json.load(json_file)
                        ta.status = 'ACCESS'
                        ta.save()
                        test_mark = Test_Mark(test=test, test_attempt=ta, 
                                  student=st, 
                                  points=test_methods.get_test_attempt_points(test_at),
                                  max_points=test_methods.get_test_points(test_f))
                        test_mark.save()
        test.status = 'CLOSED'
        test.save()      
        return redirect('course-view', id=test.course.pk)

    return render(request, 'educational/test_close.html', context={'test': test})

@login_required(login_url='/login/')
def get_course_gradebook(request, id, group_num):
    group = Study_Group.objects.get(number=group_num)
    # проверка
    context = {'id': id, 'group': group}
    context['tests'] = Test.objects.filter(status='CLOSED').order_by('publish_date')
    context['students'] = [[student, 
                            Test_Mark.objects.filter(student=student).order_by('test_attempt__test__publish_date'),
                            Test_Mark.objects.filter(student=student).order_by('test_attempt__test__publish_date').aggregate(Sum('points'))['points__sum'],
                            Test_Mark.objects.filter(student=student).order_by('test_attempt__test__publish_date').aggregate(Sum('max_points'))['max_points__sum'],
                            "%.1f" % ((Test_Mark.objects.filter(student=student).order_by('test_attempt__test__publish_date').aggregate(Sum('points'))['points__sum'] / Test_Mark.objects.filter(student=student).order_by('test_attempt__test__publish_date').aggregate(Sum('max_points'))['max_points__sum']) * 100)] for student in group.ordered_students]
    return render(request, 'educational/group_course_points.html', context)