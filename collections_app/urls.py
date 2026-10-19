from django.urls import path
from collections_app import views

app_name = "collections"

urlpatterns = [
    path("", views.collections_list, name="list"),
    path("<int:collection_id>/", views.collection_detail, name="detail"),
]
