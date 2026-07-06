from django.shortcuts import render,redirect,get_object_or_404
from myapp.models import *
from django.contrib import messages
import time



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
# Delete Action
# def delete_contact(request, id):

#     mycontact = get_object_or_404(Contact, id=id)

#     if request.method == "POST":
#         mycontact.delete()
#         messages.success(request, "Message deleted successfully.")

#     return redirect("show")


# Edit Action
def edit(request, id):

    editappointment = get_object_or_404(Contact, id=id)

    if request.method == "POST":

        editappointment.name = request.POST.get("name")
        editappointment.email = request.POST.get("email")
        editappointment.subject = request.POST.get("subject")
        editappointment.message = request.POST.get("message")

        editappointment.save()

        messages.success(request, "Message updated successfully.")

        return redirect("/show")

    else:

        return render(request, "edit.html", {
            "editappointment": editappointment
        })

# def edit(request, id):

#     editappointment = get_object_or_404(Contact, id=id)

#     if request.method == "POST":

#         editappointment.name = request.POST.get("name")
#         editappointment.email = request.POST.get("email")
#         editappointment.subject = request.POST.get("subject")
#         editappointment.message = request.POST.get("message")

#         editappointment.save()

#         messages.success(request, "Message updated successfully.")

#         return redirect("/show")

#     return render(request, "edit.html", {
#         "editappointment": editappointment
#     })


def delete (request,id):
    mycontact=Contact.objects.get(id=id)
    mycontact.delete()

    messages.success(request, "Message deleted successfully.")

    return redirect("/show")

# undo delete #
# def delete(request, id):
#     mycontact = Contact.objects.get(id=id)

#     request.session["undo_delete"] = {
#         "id": mycontact.id,
#         "name": mycontact.name,
#         "email": mycontact.email,
#         "subject": mycontact.subject,
#         "message": mycontact.message,
#         "created_at": time.time()
#     }

#     mycontact.delete()

#     messages.success(
#         request,
#         "Message deleted. You have 10 seconds to undo."
#     )

#     return redirect("/show")

# def undo_delete(request):

#     data = request.session.get("undo_delete")

#     if data:

#         if time.time() - data["created_at"] <= 10:

#             Contact.objects.create(
#                 id=data["id"],
#                 name=data["name"],
#                 email=data["email"],
#                 subject=data["subject"],
#                 message=data["message"],
#             )

#             del request.session["undo_delete"]

#             messages.success(request, "Delete undone.")

#         else:

#             del request.session["undo_delete"]

#             messages.error(request, "Undo time expired.")

#     return redirect("/show")