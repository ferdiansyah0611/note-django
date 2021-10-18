from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as loginsystem
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Todo

def is_user(user):
	if user.is_authenticated:
		return True
	else:
		return False
# Create your views here.

def index(request):
	detect = is_user(request.user)
	if detect:
		todo = []
		_from = 0
		maxpage = 10
		onnext = False
		onsearch = False
		if request.GET.get('search') is not None:
			onsearch = request.GET.get('search')
			if request.GET.get('from') is not None:
				_from = int(request.GET.get('from'))
				todo = Todo.objects.filter(user_id = request.user.id, title__contains = request.GET.get('search')).order_by('-created')[_from:maxpage + _from]
				onnext = True
			else:
				todo = Todo.objects.filter(user_id = request.user.id, title__contains = request.GET.get('search')).order_by('-created')[:maxpage]
		elif request.GET.get('from') is not None:
			_from = int(request.GET.get('from'))
			todo = Todo.objects.filter(user_id = request.user.id).order_by('-created')[_from:maxpage + _from]
			onnext = True
		else:
			todo = Todo.objects.filter(user_id = request.user.id).order_by('-created')[:maxpage]
		return render(request, "page/home.html", {
			"todo": todo,
			"from": abs(_from - maxpage),
			"to": _from + maxpage,
			"onnext": onnext,
			"onsearch": onsearch
		})
	else:
		return redirect('/login')

def create(request):
	detect = is_user(request.user)
	if detect:
		return render(request, "page/createtodo.html")
	else:
		return redirect('/login')

def edit(request, todo):
	detect = is_user(request.user)
	if detect:
		if todo:
			data = Todo.objects.get(id = todo)
			return render(request, "page/createtodo.html", {"todo": data})
		else:
			return redirect('/')
	else:
		return redirect('/login')

def delete(request, todo):
	detect = is_user(request.user)
	if detect:
		if todo:
			Todo.objects.get(id = todo).delete()
		return redirect('/')
	else:
		return redirect('/login')

def login(request):
	return render(request, "page/login.html")

def register(request):
	return render(request, "page/register.html")

def addtodo(request):
	detect = is_user(request.user)
	if detect:
		post = request.POST
		user = request.user
		title = post.get('title')
		content = post.get('content')
		created = timezone.now()
		if post.get('id'):
			data = Todo.objects.get(id = post.get('id'))
			if data:
				data.title = title
				data.content = content
				data.save()
		else:
			Todo.objects.create(user = user, title = title, content = content, created = created)
		return redirect('/')
	else:
		return redirect('/login')

def signin(request):
	post = request.POST
	user = authenticate(request, username = post.get('username'), password = post.get('password'))
	if user is not None:
		loginsystem(request, user)
		return redirect('/')
	else:
		return redirect('/login')

def signout(request):
	detect = is_user(request.user)
	if detect:
		logout(request)
		return redirect('/login')
	else:
		return redirect('/login')

def createuser(request):
	post = request.POST
	if post.get('username') and post.get('email') and post.get('password'):
		User.objects.create_user(post.get('username'), post.get('email'), post.get('password'))
		return redirect('/login')
	else:
		return redirect('/register')