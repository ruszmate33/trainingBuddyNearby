from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm, SignupForm


# Create your views here.
def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/user.html")


def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            # store userID in session (lets see if really needed)

            return HttpResponseRedirect(reverse("trainings:index"))
        # Otherwise, return login page again with new context
        else:
            loginForm = LoginForm()
            return render(request, "users/login.html", {
                "message": "Invalid Credentials",
                "loginForm":loginForm
            })
    else:
        loginForm = LoginForm()
    return render(request, "users/login.html", {"loginForm":loginForm})


def logout_view(request):
    request.session["first_name"] = []
    logout(request)
    loginForm = LoginForm()
    return render(request, "users/login.html", {
                "message": "Logged Out",
                "loginForm":loginForm
            })


# based on tutorial https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("trainings:index"))
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {
                    "form": form,
                    "message": "Sign up"
    })