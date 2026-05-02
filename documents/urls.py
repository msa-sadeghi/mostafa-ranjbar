from django.urls import path
from .views import FolderViewSet

app_name = "documents"
urlpatterns = [
    path("", FolderViewSet.as_view({"get": "list"})),
]
