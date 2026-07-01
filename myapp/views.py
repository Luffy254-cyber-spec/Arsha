from django.shortcuts import render
from myapp.models import *

# 🏠 Home page
def index(request):
    return render(request, "index.html")

# 📰 Blog page
def blog(request):
    return render(request, "blog.html")

# 🧩 Blog details page
def details(request):
    return render(request, "blog-details.html")

# ⚙️ Services page
def services(request):
    return render(request, "service-details.html")

# 🚀 Starter page
def starter(request):
    return render(request, "starter-page.html")

# ❌ Custom error page
def error(request):
    return render(request, "404.html")

def home(request):
    if request.method == 'POST':
        mycontact = Contact(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        mycontact.save()
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')