from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
# now we will access this data as the objects of the Room model
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'CP'},
#     {'id': 3, 'name': 'frontend dev'},
# ]

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.object.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is incorrect')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
        else:
            messages.error(request, 'an error occured during registration')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains = q) |
        Q(name__contains = q) |
        Q(description__contains = q) |
        Q(host__username__contains = q)
        )
    topics = Topic.objects.all()

    room_count = rooms.count()
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)

    context = {'room': room}

    return render(request, 'base/room.html', context)

@login_required(login_url='home')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='home')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='home')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})