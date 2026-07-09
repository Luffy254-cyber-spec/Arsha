from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import *
from django.contrib import messages
import time

# Mpesa API imports #
from django.http import JsonResponse
import requests
import base64
from datetime import datetime


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
    if request.method == "POST":
        mycontact = Contact(
            name=request.POST["name"],
            email=request.POST["email"],
            subject=request.POST["subject"],
            message=request.POST["message"],
        )
        mycontact.save()
        return render(request, "index.html")
    else:
        return render(request, "index.html")


def show(request):
    all = Contact.objects.all()
    return render(request, "show.html", {"all": all})


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

        return render(request, "edit.html", {"editappointment": editappointment})


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


def delete(request, id):
    mycontact = Contact.objects.get(id=id)
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


# Mpesa Views#
# ─────────────────────────────────────────────
#  M-Pesa Daraja API Credentials (Sandbox)
#  Get these from: https://developer.safaricom.co.ke
# ─────────────────────────────────────────────
CONSUMER_KEY = "DFNNhTN9AjISate6ZO3YDHNSTinbxNDLKCr7D7Ce5IFGEv6a"
CONSUMER_SECRET = "8yyhSAJO0JcVP9Nnf8q2AAmKcHldPXD0dqBwUKuGMZGiAHYqTczfi2obDrHG6J23"
SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CALLBACK_URL = (
    "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
)


# ─────────────────────────────────────────────
#  STEP 1: Get Access Token
#  Every M-Pesa request needs a token first.
# ─────────────────────────────────────────────
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=30)
    token = response.json()["access_token"]
    return token


# ─────────────────────────────────────────────
#  STEP 2: Send STK Push (Payment Prompt)
#  This sends a pop-up to the customer's phone.
# ─────────────────────────────────────────────
def stk_push(phone, amount):
    token = get_access_token()

    # Timestamp format required by Safaricom: YYYYMMDDHHmmss
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Password = Base64(Shortcode + Passkey + Timestamp)
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "BusinessShortCode": SHORTCODE,  # Your till/paybill number
        "Password": password,  # Generated above
        "Timestamp": timestamp,  # Current time
        "TransactionType": "CustomerPayBillOnline",  # Use "CustomerBuyGoodsOnline" for till
        "Amount": amount,  # Amount to charge
        "PartyA": phone,  # Customer phone e.g. 2547XXXXXXXX
        "PartyB": SHORTCODE,  # Your shortcode receives the money
        "PhoneNumber": phone,  # Phone that gets the STK prompt
        "CallBackURL": CALLBACK_URL,  # M-Pesa sends result here
        "AccountReference": "Biashara",  # Shows on customer's phone
        "TransactionDesc": "Payment",  # Short description
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return response.json()


# ─────────────────────────────────────────────
#  VIEWS/FUNCTIONS
# ─────────────────────────────────────────────


def payment(request):
    """Show payment form (GET) or trigger STK push (POST)."""

    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        amount = request.POST.get("amount", "").strip()

        try:
            result = stk_push(phone, amount)
            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=503)

    # GET request → show the payment form
    return render(request, "payment.html")


def callback(request):
    """M-Pesa sends payment results here after the customer pays."""
    print("M-Pesa Callback:", request.body)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
