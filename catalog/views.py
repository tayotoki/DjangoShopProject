from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    ctx = {
        "form_valid": True,
        "feedback_complete": False,
        "form": {
          "user_name": "",
          "user_feedback": "",
        },
        "items": [
            {
                "id": "one",
                "title": "Где мы находимся",
                "answer": "ул. Пушкина, д. Колотушкина"
            },
            {
                "id": "two",
                "title": "Связаться с нами через соц. сети",
                "answer": "12345 12345 12345 12345"
            }

        ]
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
