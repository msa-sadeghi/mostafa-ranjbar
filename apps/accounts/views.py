from django.shortcuts import render
from .models import User
from django.http import JsonResponse
from django.views.generic.list import ListView


# def users(request):
#     users = User.objects.all().values()
#     return JsonResponse(list(users), safe=False)

def users(request):
    users = User.objects.all()
    return render(request, "accounts/users_list.html", {"users": users})


class UsersView(ListView):
    model = User
    template_name = "accounts/users_list.html"
    context_object_name = "users"


# class UserViewSet()