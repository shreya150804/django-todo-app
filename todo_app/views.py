from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo_app import models
from todo_app.models import Todo
from django.contrib.auth import authenticate,login as Auth_login,logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method=="POST":
        fnm=request.POST.get("fnm")
        emailid=request.POST.get("email")
        pwd=request.POST.get("pwd")
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save
        return redirect("/login")
    return render(request,"signup.html")

def login(request):
    if request.method=="POST":
        fnm=request.POST.get("fnm")
        pwd=request.POST.get("pwd")
        print(fnm,pwd)
        user=authenticate(request,username=fnm,password=pwd)
        if user is not None:
            Auth_login(request, user)
            return redirect("/todopage")
        else:
            return redirect("/login", {'error': 'Invalid credentials'})
    return render(request,"login.html")

@login_required(login_url='/login/')
def todopage(request):
    if request.method=="POST":
        title=request.POST.get("title")
        print(title)
        obj=models.Todo(title=title, user=request.user)
        obj.save()
        res=models.Todo.objects.filter(user=request.user).order_by("-date")
        return redirect("/todopage",{"res":res})
    res=models.Todo.objects.filter(user=request.user).order_by("-date")
    return render(request,"todo.html",{'res':res})

@login_required(login_url='/login/')
def edittodo(request,srno):
    if request.method=="POST":
        title=request.POST.get("title")
        print(title)
        obj=models.Todo.objects.get(srno=srno)
        obj.title=title
        obj.save()
        return redirect("/todopage",{'obj':obj})
    obj=models.Todo.objects.get(srno=srno)
    res=models.Todo.objects.filter(user=request.user).order_by("-date")
    return render(request,"edittodo.html")

@login_required(login_url='/login/')
def delete(request,srno):
    obj=models.Todo.objects.get(srno=srno)
    obj.delete()
    return redirect("/todopage")

def signout(request):
    logout(request)
    return redirect('/login')