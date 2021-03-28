from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):

    if request.method == 'GET':
        return render(request, 'woo/signup.html', {'form':UserCreationForm(),'name':'Register'})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('login')
            except IntegrityError:
                return render(request,'woo/signup.html',{'form':UserCreationForm(),'error':'username already taken','name':'Register'})
        else:
            return render(request,'woo/signup.html',{'form':UserCreationForm(),'error':'Password don\'t match','name':'Register'})

@login_required
def current(request):
    todos = Todo.objects.filter(author=request.user,datecompleted__isnull=True)
    return render(request,'woo/current.html',{'todos':todos,'name':'Todos-to-complete'})


@login_required
def viewTodo(request,pk):
    todo = get_object_or_404(Todo,pk=pk,author=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,'woo/viewTodo.html',{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request,'woo/viewTodo.html',{'todo':todo,'form':form,'error':'Bad info'})



def loginuser(request):
    if request.method == 'GET':
        return render(request, 'woo/login.html', {'form':AuthenticationForm(),'name':'Login'})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'woo/login.html',{'form':AuthenticationForm(),'error':'username and password don\'t match','name':'Register'})
        else:
            login(request,user)
            return redirect('current')
@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'woo/createtodo.html', {'form':TodoForm(),'name':'Create'})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo=form.save(commit=False)
            newTodo.author=request.user
            newTodo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'woo/createtodo.html', {'form':TodoForm(),'error':'Bad data cause this error','name':'Create'})
@login_required
def complete(request,pk):
    todo=get_object_or_404(Todo,pk=pk,author=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current')
@login_required
def delete(request,pk):
    todo=get_object_or_404(Todo,pk=pk,author=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('current')
@login_required
def completed(request):
    todos = Todo.objects.filter(author=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'woo/completed.html',{'todos':todos,'name':'Completed'})



@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
