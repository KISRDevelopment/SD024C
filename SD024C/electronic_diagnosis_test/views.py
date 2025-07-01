from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"index.html")

def about (request):
    return render (request,"about.html")

def help (request):
    return render (request,"help.html")

def contact (request):
    return render (request,"contact.html")

def login (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.user.is_staff:
                return HttpResponseRedirect("superusers")
            else:
                return HttpResponseRedirect("students")

        else:
            messages.info(request, 'Invalid Username or Password')
            return HttpResponseRedirect("login")
    else:
        return render(request, "login.html")