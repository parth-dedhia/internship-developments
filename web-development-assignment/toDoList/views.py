from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate 
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList
from django.contrib.auth.models import User
import datetime

# Create your views here.
@login_required
def toDoList(request):
    email = request.user.email
    name = request.user.username
    user = User.objects.get(username = name)
    details = user.todolist_set.order_by('-priority').all()
    # details.sort(key=lambda x: x.count, reverse=True)
    return render(request,'toDoList/list.html',{'details':details , 'day': datetime.datetime.today().strftime("%A"), 'date': datetime.date.today() , 'name':name})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def mailPage(request):
    return render(request,'toDoList/mail.html')

@login_required
def mailSelf(request):
    subject  = "To Do List of User " + request.user.username
    # send_to = request.POST['email_id']
    
    send_to = request.user.email

    name = request.user.username
    user = User.objects.get(username = name)
    details = user.todolist_set.all()
    work_list = ''
    for detail in details:
        temp = detail.task + " : " + detail.status + "\n"
        work_list = work_list + temp
    message = request.POST['selfMail'] + '\n\n' + work_list
    if subject and send_to:
        try:
            send_mail(subject, message, 'parthdedhiablogs@gmail.com', [send_to,])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

@login_required
def mailOthers(request):
    subject  = "To Do List of User " + request.user.username
    send_to = request.POST['email_id']
    
    email = request.user.email
    name = request.user.username
    user = User.objects.get(username = name)
    details = user.todolist_set.all()
    work_list = ''
    for detail in details:
        temp = detail.task + " : " + detail.status + "\n"
        work_list = work_list + temp
    message = request.POST['othermail'] + '\n\n' + work_list
    if subject and send_to:
        try:
            send_mail(subject, message, 'parthdedhiablogs@gmail.com', [send_to,])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

@login_required
def addTask(request):
    name = request.user.username
    user = User.objects.get(username = name)
    priority = request.POST['inlineRadioOptions']
    status = "INCOMPLETE"
    task = request.POST['task']
    detail = ToDoList(user = user, task = task , status = status , priority = priority)
    detail.save()
    return redirect('/')

@login_required
def taskCompleted(request):
    name = request.user.username
    user = User.objects.get(username = name)
    task_id = request.POST['completedTask']
    print(task_id)
    details = user.todolist_set.get(id=task_id)
    details.status = "COMPLETE"
    details.priority = 0
    details.save()
    # return True
    return redirect('/')

@login_required
def deleteCompletedTask(request):
    name = request.user.username
    user = User.objects.get(username = name)
    tasks = user.todolist_set.filter(status="COMPLETE")
    tasks.delete()
    return redirect('/')

@login_required
def deleteAllTasks(request):
    name = request.user.username
    user = User.objects.get(username = name)
    tasks = user.todolist_set.all()
    tasks.delete()
    return redirect('/')
    