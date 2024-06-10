from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import SwitForm
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
    else:
        profiles = Profile.objects.all()

    return render(request, "profile_list.html", {"profiles":profiles})

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
        profiles = Profile.objects.all()
        messages.success(request, "Login Or Register To View Profiles?")
        return render(request, "profile_list.html", {"profiles":profiles})
