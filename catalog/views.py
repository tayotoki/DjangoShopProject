from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product, Category, Contact


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    last_five_products = Product.objects.all()[:5]

    ctx = {
        "last_five_products": last_five_products,
    }
    return render(request=request, template_name="home.html", context=ctx)


def contacts(request: HttpRequest) -> HttpResponse:
    contacts = Contact.objects.all()

    ctx = {
        "form_valid": True,
        "feedback_complete": False,
        "form": {
          "user_name": "",
          "user_feedback": "",
        },
        "items": contacts,
    }

    if request.method == "POST":
        if not all(
            (user_name := request.POST.get("user_name"),
             user_feedback := request.POST.get("user_feedback"))
        ):
            ctx["form_valid"] = False
            ctx["form"]["user_name"] = user_name
            ctx["form"]["user_feedback"] = user_feedback
        else:
            ctx["feedback_complete"] = True

    return render(request, "contacts.html", context=ctx)
