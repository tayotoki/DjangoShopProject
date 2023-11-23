from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from .models import Product, Contact
from .forms import ProductForm


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by("-modified_at")

    default_page = 1
    page = request.GET.get("page", default_page)

    items_per_page = 8
    paginator = Paginator(products, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    ctx = {
        "products": items_page
    }

    return render(request=request, template_name="home.html", context=ctx)


def product(request: HttpRequest, pk: int) -> HttpResponse:

    product = get_object_or_404(Product, pk=pk)

    ctx = {
        "product": product
    }

    return render(request, template_name="product.html", context=ctx)


def create_product(request: HttpRequest):
    form = ProductForm()

    ctx = {
        "form": form
    }

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("catalog:index")
        else:
            ctx["form"] = form

    return render(request=request, template_name="create_product.html", context=ctx)


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
