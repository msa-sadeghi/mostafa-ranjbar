from django.shortcuts import render
from .models import User
from django.http import JsonResponse
from django.views.generic.list import ListView

# def users(request):
#     users = User.objects.all().values()
#     return JsonResponse(list(users), safe=False)

# def users(request):
#     users = User.objects.all()
#     return render(request, "accounts/users_list.html", {"users": users})


# class UsersView(ListView):
#     model = User
#     template_name = "accounts/users_list.html"
#     context_object_name = "users"


# class UserViewSet()


from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserListSerializer, UserDetailSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer

        return UserDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=["get"], url_path="me")
    def my_profile(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="register", permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "registration done successfully", "user_id": user.id})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        if not request.user.is_admin:
            return Response({"error": "you dont have permissions"}, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        user.is_active = not user.is_active

        user.save(update_fields=["is_active"])

        return Response({"message": f"operation done", "is_active": user.is_active})
