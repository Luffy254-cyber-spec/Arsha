from django.shortcuts import render,redirect,get_object_or_404
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

def show(request):
    all=Contact.objects.all()
    return render(request,'show.html',{'all':all})


# delete action #
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect("show")

# edit action#
def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        contact.name = request.POST.get("name")
        contact.email = request.POST.get("email")
        contact.subject = request.POST.get("subject")
        contact.message = request.POST.get("message")
        contact.save()
        return redirect("show")
    return redirect("show")