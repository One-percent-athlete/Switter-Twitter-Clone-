from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm, SwitForm
from .models import Profile, Swit

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = SwitForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                swit = form.save(commit=False)
                swit.user = request.user
                swit.save()
                messages.success(request, "Thank You For Your Swit!")
                return redirect("home")
            
        swits = Swit.objects.all().order_by("-create_at")
        return render(request, "home.html", {"swits":swits,"form":form})
    else:
        swits = Swit.objects.all().order_by("-create_at")
        return render(request, "home.html", {"swits":swits})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles":profiles})
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")
    

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=pk)
        swits = Swit.objects.filter(user_id=pk).order_by("-create_at")
        if request.method == "POST":
            current_user = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                current_user.follows.remove(profile)
            elif action == "follow":
                current_user.follows.add(profile)
            current_user.save()
        return render(request, "profile.html", {"profile":profile, "swits":swits})
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")
    

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
             messages.success(request, "Welcome Back. Ready For Some Swits?")
             return redirect("home")
        else:
             messages.success(request, "Something Went Wrong. Please Try Again.")
             return redirect("login")
    else:   
        return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "See You Later..")
    return redirect("home")

def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Welcome! Ready To Post Some Swits?")
            return redirect("home")
       
    return render(request, "register.html", {"form":form})

