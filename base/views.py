from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Python"},
#     {"id": 2, "name": "Cpp"},
# ]


def LoginPage(request):
    page = "Login"

    if request.user.is_authenticated:
        return redirect("Home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesnt exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "Username Or Password Is Wrong")

    context = {"page": page}
    return render(request, "base/log_reg.html", context)


def Home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    roomCount = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "roomCount": roomCount,
        "room_messages": room_messages,
    }
    return render(request, "base/Home.html", context)


def room(request, no):
    room = Room.objects.get(id=no)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", no=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, no):
    user = User.objects.get(id=no)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="Login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            user=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("Home")
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.user = request.user
        #     room.save()

    context = {"form": form, "topics": topics}
    return render(request, "base/create.html", context)


@login_required(login_url="Login")
def updateRoom(request, no):
    room = Room.objects.get(id=no)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.user:
        return HttpResponse("Only Owner can update the room")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.save()
        room.description = request.POST.get("description")
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect("Home")
    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/create.html", context)


@login_required(login_url="Login")
def deleteRoom(request, no):
    room = Room.objects.get(id=no)

    if request.user != room.user:
        return HttpResponse("Only Owner can delete the room")

    if request.method == "POST":
        room.delete()
        return redirect("Home")
    return render(request, "base/delete.html", {"obj": room})


def LogoutPage(request):
    logout(request)
    return redirect("Home")


def RegisterPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("Home")

        else:
            messages.error(request, "An Error Occured during registration")

    context = {"form": form}
    return render(request, "base/log_reg.html", context)


@login_required(login_url="Login")
def deleteMessage(request, no):
    message = Message.objects.get(id=no)

    if request.user != message.user:
        return HttpResponse("Only Owner can delete the room")

    if request.method == "POST":
        message.delete()
        return redirect("Home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="Login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", no=user.id)

    context = {"form": form}
    return render(request, "base/updateUser.html", context)


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, "base/topics.html", context)
