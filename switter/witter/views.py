from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from witter.forms import SwitForm, SignUpForm, UpdateUserForm, ChangePasswordForm, ProfileForm
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
        profiles = Profile.objects.all()
        return render(request, "home.html", {"swits":swits,"form":form, "profiles":profiles})
    else:
        swits = Swit.objects.all().order_by("-create_at")
        profiles = Profile.objects.all()
        return render(request, "home.html", {"swits":swits, "profiles":profiles})

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


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_profile = Profile.objects.get(user__id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            profile = Profile.objects.get(id=current_user.id)
            swits = Swit.objects.filter(user_id=current_user.id).order_by("-create_at")
            messages.success(request, "You Profile Has Been Updated!")
            return render(request, "profile.html", {"profile":profile, "swits":swits})
        return render(request, "update_user.html", {"user_form": user_form, "profile_form": profile_form, "current_user": current_user})
    else:
        messages.success(request, "Do You Want To Register Or Login First?")
        return redirect("home")

def update_password(request, pk):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=pk)
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password Has Been Updated Successfully. Please Login Again.")
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password", pk)
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html",{"form": form, "pk": pk})
    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")

def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        
        current_user = request.user.profile
        current_user.follows.add(profile)
        current_user.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")

def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        
        current_user = request.user.profile
        current_user.follows.remove(profile)
        current_user.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")
    
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            user_profile = Profile.objects.get(user_id=pk)
            return render(request, "follows.html", {"user_profile": user_profile})
        else:

            messages.success(request, "That's Not Your Profile!")
            return redirect("home") 
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            user_profile = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"user_profile": user_profile})
        else:
            messages.success(request, "That's Not Your Profile!")
            return redirect("home") 
    else:
        messages.success(request, "Login Or Register To View Profiles?")
        return redirect("home")
    
def swit_like(request, pk):
    if request.user.is_authenticated:
        swit = get_object_or_404(Swit, id=pk)
        if swit.likes.filter(id=request.user.id):
            swit.likes.remove(request.user)
        else:
            swit.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")
    
def swit_show(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                current_user.follows.remove(profile)
            elif action == "follow":
                current_user.follows.add(profile)
            current_user.save()
        swit = get_object_or_404(Swit, id=pk)
        profile = Profile.objects.get(id=swit.user.id)

        return render(request, "swit_show.html", {"swit": swit, "profile":profile})

    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")


def delete_swit(request, pk):
    if request.user.is_authenticated:
        swit = get_object_or_404(Swit, id=pk)
        if request.user.username == swit.user.username:
            swit.delete()
            messages.success(request, "Swit Deleted Succesfully!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, "It's Not Your Swit!")
            return redirect("home")
        pass
    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")
        
def edit_swit(request, pk):
    if request.user.is_authenticated:
        swit = get_object_or_404(Swit, id=pk)
        if request.user.username == swit.user.username:
            form = SwitForm(request.POST or None, instance=swit)
            if request.method == "POST":
                if form.is_valid():
                    swit = form.save(commit=False)
                    swit.user = request.user
                    swit.save()
                    messages.success(request, "Your Swit Has Been Updated!")
                    return redirect("home")
            else:
                return render(request, "edit_swit.html", {"form": form,"swit": swit})

        else:
            messages.success(request, "It's Not Your Swit!")
            return redirect("home")
    else:
        messages.success(request, "You Have To Login First.")
        return redirect("home")
        
def search_swit(request):
    if request.method == "POST":
        keyword = request.POST["search"]
        swits = Swit.objects.filter(body__contains=keyword)
        return render(request, "search_swit.html", {"swits":swits, "keyword":keyword})
    else:
        return render(request, "search_swit.html")
        
def search_user(request):
    if request.method == "POST":
        keyword = request.POST["search"]
        users = User.objects.filter(username__contains=keyword)
        return render(request, "search_user.html", {"users":users, "keyword":keyword})
    else:
        return render(request, "search_user.html")
        
