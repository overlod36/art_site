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
from .models import Course, Lecture, Test, Test_Question, Test_Answer, Test_Attempt, Test_Attempt_Answer, Task, Task_Attempt, Task_Attempt_File
from informing_app.models import Course_Announce
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from users.models import Teacher_Profile, Student_Profile, Study_Group
from .decorators import check_course_existence, course_access, check_test_existence
from .forms import (TestForm, TaskForm, TestShowForm, 
                    TestAttemptCheckForm, AttemptDeniedForm, TestInfoForm, 
                    TestQuestionForm, TestPublishForm, TaskAttemptFilesForm, 
                    TaskAttemptAcceptForm, TestDeleteForm, TestCloseForm, TaskAttemptDeniedForm)
from django.http import HttpRequest
from django.shortcuts import redirect
import json
from . import test_methods
from . import file_methods
import os
from django.core.files import File
from django.db.models import Sum
from django.db.models import Q
from django.views.decorators.cache import cache_control

class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    template_name = 'educational/lecture_create.html'
    fields = ['file']

    def get_form(self, form_class=None):
        if form_class is None: form_class = self.get_form_class()

        form = super(LectureCreateView, self).get_form(form_class)
        form.fields['file'].label = ''
        form.fields['file'].widget.attrs['class'] = 'form-control mb-4'
        
        return form

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

    def get_form(self, form_class=None):
        if form_class is None: form_class = self.get_form_class()

        form = super(CourseCreateView, self).get_form(form_class)
        form.fields['title'].widget.attrs['placeholder'] = 'Название дисциплины'
        form.fields['title'].label = ''
        form.fields['title'].widget.attrs['class'] = 'form-control mb-2'
        form.fields['groups'].label=''
        form.fields['groups'].widget.attrs['placeholder'] = 'Группы' 
        form.fields['groups'].widget.attrs['class'] = 'form-select mb-2'
        form.fields['description'].label = ''
        form.fields['description'].widget.attrs['class'] = 'form-control'
        return form

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

class TestCreateView(LoginRequiredMixin, CreateView):
    form_class = TestForm
    template_name = 'educational/test_create.html'
 
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['id']
            return super(TestCreateView, self).dispatch(request)
    
    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.pk)
        return super().form_valid(form)
        
class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'educational/task_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['course_id']
            return super(TaskCreateView, self).dispatch(request)

    def get_success_url(self):
        return reverse('course-view', kwargs={'id': self.pk})

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.pk)
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    template_name = 'educational/task_update.html' 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['pk']
            self.course = kwargs['course_id']
            return super(TaskUpdateView, self).dispatch(request)

    def get_success_url(self):
        return reverse('course-view', kwargs={'id': self.course})
    
    def get_queryset(self):
        instance = Task.objects.filter(pk=self.pk)
        return instance

    def form_valid(self, form):
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'educational/task-delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.course = kwargs['course_id']
            return super(TaskDeleteView, self).dispatch(request)

    def get_success_url(self) -> str:
        return reverse('course-view', kwargs={'id': self.course})

@login_required(login_url='/login/')
def task_close(request, course_id, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.status = 'CLOSED'
        task.save(update_fields=['status'])
        return redirect('course-view', course_id)
    return render(request, 'educational/task-close.html', context={'c_id': course_id})

@login_required(login_url='/login/')
def task_publish(request, course_id, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        # либо 0 баллов всем непроверенным, либо запрещать закрывать тест
        task.status = 'DONE'
        task.save(update_fields=['status'])
        return redirect('course-view', course_id)
    return render(request, 'educational/task-publish.html', context={'c_id': course_id})

@login_required(login_url='/login/')
def get_task_attempts(request, course_id, task_id):
    context = {'students':[], 'course_id': course_id, 'task_id': task_id}
    task = Task.objects.get(pk=task_id)
    attempts = Task_Attempt.objects.filter(task=task)
    for student in Student_Profile.objects.filter(group__in=task.course.groups.all()):
        context['students'].append([student, Task_Attempt.objects.filter(Q(task=task) & Q(student=student))])
    return render(request, 'educational/task-attempts-list.html', context)

@login_required(login_url='/login/')
def get_task_attempt(request, course_id, task_id, attempt_id):
    attempt = Task_Attempt.objects.get(pk=attempt_id)
    files = attempt.task_attempt_file_set.all()
    return render(request, 'educational/task_attempt.html', context={'files': files,
                                                                     'c_id': course_id,
                                                                     'task_id': task_id,
                                                                     'a_id': attempt_id,
                                                                     'comment': attempt.comment})
                                                                           
@login_required(login_url='/login/')
def send_task_attempt(request, course_id, task_id):
    if Task_Attempt.objects.filter(Q(student=request.user.student_profile)&Q(task=Task.objects.get(pk=task_id))).filter(Q(status='CHECK')|Q(status='ACCESS')):
        return redirect('course-view', course_id)
    form = TaskAttemptFilesForm()
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        attempt = Task_Attempt(task=task, 
                               student=request.user.student_profile,
                               status="CHECK",
                               mark=0)
        attempt.save()
        if request.FILES:
            for file in request.FILES.getlist('files'):
                task_file = Task_Attempt_File(task_attempt=attempt,
                                              file=file)
                task_file.save()
        return redirect('course-view', course_id)

    return render(request, 'educational/task_attempt_create.html', context={'form': form})

@login_required(login_url='/login/')
def get_task_attempt_file(request, course_id, task_id, attempt_id, file_id):
    file = Task_Attempt_File.objects.get(pk=file_id)
    resp = HttpResponse(file.file, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{ file.filename }"'
    return resp

@login_required(login_url='/login/')
def check_task_attempt(request, course_id, task_id, attempt_id):
    attempt = Task_Attempt.objects.get(pk=attempt_id)
    files = attempt.task_attempt_file_set.all()
    denied = TaskAttemptDeniedForm()
    accept = TaskAttemptAcceptForm(attempt.task.mark)

    if request.method == 'POST':
        if 'denied_st' in request.POST:
            attempt.status = 'DENIED'
            attempt.comment = request.POST['comment']
            attempt.save(update_fields=['status', 'comment'])
        elif 'accepted_st' in request.POST:
            res = request.POST
            attempt.status = 'ACCESS'
            attempt.mark = int(res['mark'][0])
            attempt.comment = res['comment']
            attempt.save(update_fields=['status', 'mark', 'comment'])
        return redirect('task-attempts', course_id, task_id)

    return render(request, 'educational/task_attempt_check.html', context={'denied':denied,
                                                                           'accept': accept,
                                                                           'files': files,
                                                                           'c_id': course_id,
                                                                           'task_id': task_id,
                                                                           'a_id': attempt_id})

@login_required(login_url='/login/')
def delete_question(request, course_id, test_id, pk):
    question = Test_Question.objects.get(pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('test-update', course_id=course_id, test_id=test_id)
    return render(request, 'educational/question_delete.html')

@login_required(login_url='/login/')
def get_lecture(request, id):
    lecture = Lecture.objects.get(pk=id)
    resp = HttpResponse(lecture.file, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{ lecture.filename }"'
    return resp

@login_required(login_url='/login/')
def get_test_attempts(request, course_id, test_id):
    test = Test.objects.get(pk=test_id)
    context = {'students':[], 'course_id': course_id, 'test': test, 'form': TestCloseForm()}
    attempts = Test_Attempt.objects.filter(test=test)
    for student in Student_Profile.objects.filter(group__in=test.course.groups.all()):
        context['students'].append([student, Test_Attempt.objects.filter(Q(test=test) & Q(student=student))])
    if request.method == 'POST':
        if 'close_st' in request.POST:
            # проверка если есть попыт + окно уведомления
            test.status = 'CLOSED'
            test.save(update_fields=['status'])
            return redirect('course-view', course_id)
    return render(request, 'educational/test-attempt-list.html', context)

@login_required(login_url='/login/')
def get_test_attempt(request, course_id, test_id, attempt_id):
    attempt = Test_Attempt.objects.get(pk=attempt_id)
    answers = []
    for answer in attempt.test_attempt_answer_set.all():
        points = 0
        if answer.is_correct: points = answer.question.mark
        answers.append([answer.question.text, answer.answer, [ans.text for ans in answer.question.test_answer_set.filter(is_correct=True)][0], answer.question.mark, points])
    return render(request, 'educational/test_attempt.html', context={'answers': answers})

@login_required(login_url='/login/')
def check_test_attempt(request, course_id, test_id, attempt_id):
    attempt = Test_Attempt.objects.get(pk=attempt_id)
    form = TestAttemptCheckForm(attempt)
    denied = AttemptDeniedForm()
    answers = [[answer.question.text, answer.answer, [ans.text for ans in answer.question.test_answer_set.filter(is_correct=True)][0], answer.question.mark, str(answer.question.pk)] for answer in attempt.test_attempt_answer_set.all()]

    if request.method == 'POST':
        if 'denied_st' in request.POST:
            attempt.status = 'DENIED'
            attempt.mark = 0
            attempt.save(update_fields=['status', 'mark'])
            return redirect('test-attempts', course_id=course_id, test_id=test_id)
        else:
            res = dict(request.POST)
            del res['csrfmiddlewaretoken']
            total_points = 0
            for key in res: total_points += int(res[key][0])
            attempt.status = 'ACCESS'
            attempt.mark = total_points
            attempt.save(update_fields=['status', 'mark'])
            return redirect('test-attempts', course_id=course_id, test_id=test_id)


    return render(request, 'educational/test_attempt_check.html', context={'form': form, 
                                                                           'attempt': attempt,
                                                                           'answers': answers,
                                                                           'denied': denied})

@login_required(login_url='/login/')
def render_test(request, course_id, test_id):
    test = Test.objects.get(pk=test_id)
    form = TestShowForm(test=test)

    if request.method == 'POST':
        res = dict(request.POST)
        del res['csrfmiddlewaretoken']
        test_attempt = Test_Attempt(test=test, student=request.user.student_profile, status='CHECK', mark=0)
        test_attempt.save()
        total_points = 0
        for key in res:
            correct = False
            question = Test_Question.objects.get(pk=int(key))
            true_answers = [ans.text for ans in question.test_answer_set.filter(is_correct=True)]
            answers = res[key]
            if sorted(true_answers) == sorted(answers):
                total_points += int(question.mark)
                correct = True
            attempt_answer = Test_Attempt_Answer(test_attempt=test_attempt, question=question, answer=answers[0], is_correct=correct)
            attempt_answer.save()
        test_attempt.mark = total_points
        test_attempt.save(update_fields=['mark'])
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': return HttpResponse(json.dumps({'status': 1}), content_type='application/json')
        else:  return redirect('course-view', id=course_id)
    return render(request, 'educational/test_sample.html', context={'form':form, 'time': test.duration.total_seconds()})

@login_required(login_url='/login/')
def update_test(request, course_id, test_id):
    test = Test.objects.get(pk=test_id)
    InfoForm = TestInfoForm(instance=test)
    QuestionForm = TestQuestionForm()
    PublishForm = TestPublishForm()
    DeleteForm = TestDeleteForm()

    if request.method == 'POST':
        print(request.POST)
        if 'publish_st' in request.POST:
            # проверка на кол-во вопросов
            test.status = 'DONE'
            test.save(update_fields=['status'])
            return redirect('course-view', id=course_id)
        elif 'delete_st' in request.POST:
            test.delete()
            return redirect('course-view', id=course_id)
        elif 'question_st' in request.POST:
            question = dict(request.POST)
            del question['csrfmiddlewaretoken']
            del question['question_st']
            # if True not in question['answer_correction']
            test_question = Test_Question(test=test, text=question['text'][0], mark=int(question['mark'][0]))
            test_question.save()
            if len(question['answer']) == 1:
                test_answer = Test_Answer(question=test_question, 
                                          text=question['answer'][0], 
                                          is_correct=True)
                test_answer.save()
            else:
                for answer in zip(question['answer'], question['answer_correction']):
                    test_answer = Test_Answer(question=test_question,
                                              text=answer[0],
                                              is_correct=answer[1])
                    test_answer.save()
        elif 'info_st' in request.POST:
            question = dict(request.POST)
            del question['csrfmiddlewaretoken']
            del question['info_st']
            test.title = question['title'][0]
            test.duration = question['duration'][0]
            test.save(update_fields=['title', 'duration'])
        return redirect('test-update', course_id=course_id, test_id=test_id)

    return render(request, 'educational/test_update.html', context={'q_form': QuestionForm,
                                                                    'info_form': InfoForm,
                                                                    'publish_form': PublishForm,
                                                                    'delete_form': DeleteForm,
                                                                    'test': test})

@login_required(login_url='/login/')
@check_course_existence
@course_access
def get_course(request, id):
    f_course = Course.objects.filter(pk=id).first()
    return render(request, 'educational/course.html', 
                  {'course': f_course, 
                   'lectures': Lecture.objects.filter(course=f_course).all(),
                   'announces': Course_Announce.objects.filter(course=f_course).order_by('-publish_date'),
                   'tests': Test.objects.filter(course=f_course).all(),
                   'tasks': Task.objects.filter(course=f_course).all()})

@login_required(login_url='/login/')
# @check_test_existence
# доступ
def get_test(request, course_id, test_id):
    test = Test.objects.get(pk=test_id)
    if hasattr(request.user, 'teacher_profile'):
        if test.course.author == request.user.teacher_profile:
            if test.status == 'PROCESS':
                return redirect('test-update', course_id=course_id, test_id=test_id)
            else:
                return redirect('test-attempts', course_id=course_id, test_id=test_id)
    elif hasattr(request.user, 'student_profile'):
        if not Test_Attempt.objects.filter(Q(student=request.user.student_profile)&Q(test=test)).filter(Q(status='ACCESS') | Q(status='CHECK')):
            return redirect('test-render', course_id=course_id, test_id=test_id)
        return redirect('course-view', id=course_id)
    return render(request, 'educational/test_sample.html')

@login_required(login_url='/login/')
def get_student_gradebook(request, student_id):
    # проверка на препода или конкретного ученика 
    student = Student_Profile.objects.get(pk=student_id)
    courses = Course.objects.filter(groups=student.group)
    result = []
    for course in courses:
        st_tests = []
        st_tasks = []
        tests = Test.objects.filter(course=course).filter(Q(status='DONE')|Q(status='CLOSED')).order_by('publish_date')
        tasks = Task.objects.filter(course=course).filter(Q(status='DONE')|Q(status='CLOSED')).order_by('publish_date')
        for test in tests:
            attempts = Test_Attempt.objects.filter(Q(test=test)&Q(student=student))
            if attempts:
                if attempts.filter(status='ACCESS'):
                    st_tests.append([test, attempts.get(status='ACCESS')])
                elif attempts.filter(status='CHECK'):
                    st_tests.append([test, 'check'])
                else:
                    st_tests.append([test, 'to_solve'])
            else:
                if test.status == 'CLOSED':
                    st_tests.append([test, 'skipped'])
                else:
                    st_tests.append([test, 'to_solve'])
        for task in tasks:
            attempts = Task_Attempt.objects.filter(Q(task=task)&Q(student=student))
            if attempts:
                if attempts.filter(status='ACCESS'):
                    st_tasks.append([task, attempts.get(status='ACCESS')])
                elif attempts.filter(status='CHECK'):
                    st_tasks.append([task, 'check'])
                else:
                    st_tasks.append([task, 'to_solve'])
            else:
                if task.status == 'CLOSED':
                    st_tasks.append([task, 'skipped'])
                else:
                    st_tasks.append([task, 'to_solve'])
        result.append([course, st_tests, st_tasks])
    return render(request, 'educational/student_gradebook.html', context={'courses': result})



@login_required(login_url='/login/')
def get_global_gradebook(request, teacher_id):
    teacher = Teacher_Profile.objects.get(pk=teacher_id)
    courses = Course.objects.filter(author=teacher)
    result = []
    for course in courses:
        # если нет групп
        tests = Test.objects.filter(course=course).filter(Q(status='DONE')|Q(status='CLOSED')).order_by('publish_date')
        tasks = Task.objects.filter(course=course).filter(Q(status='DONE')|Q(status='CLOSED')).order_by('publish_date')
        course_groups = []
        for group in course.groups.all():
            group_list=[]
            for student in group.student_profile_set.all():
                student_scores = [student, [], [], [], []]
                for test in tests:
                    test_closed = 2
                    if test.status == 'CLOSED': test_closed = 1
                    attempts = Test_Attempt.objects.filter(Q(test=test)&Q(student=student))
                    if attempts:
                        if attempts.filter(status='ACCESS'):
                            student_scores[test_closed].append(attempts.get(status='ACCESS'))
                        elif attempts.filter(status='CHECK'):
                            student_scores[test_closed].append(attempts.get(status='CHECK'))
                    else:
                        student_scores[test_closed].append('no_att')
                for task in tasks:
                    task_closed = 4
                    if task.status == 'CLOSED': task_closed = 3
                    attempts = Task_Attempt.objects.filter(Q(task=task)&Q(student=student))
                    if attempts:
                        if attempts.filter(status='ACCESS'):
                            student_scores[task_closed].append(attempts.get(status='ACCESS'))
                        elif attempts.filter(status='CHECK'):
                            student_scores[task_closed].append(attempts.get(status='CHECK'))
                    else:
                        student_scores[task_closed].append('no_att')
                group_list.append(student_scores)
            course_groups.append([group, group_list, 
                                  Test.objects.filter(course=course).filter(status='CLOSED').order_by('publish_date'),
                                  Test.objects.filter(course=course).filter(status='DONE').order_by('publish_date'),
                                  Task.objects.filter(course=course).filter(status='CLOSED').order_by('publish_date'),
                                  Task.objects.filter(course=course).filter(status='DONE').order_by('publish_date')])
        result.append([course, course_groups])
    return render(request, 'educational/global_gradebook.html', context={'courses': result})

