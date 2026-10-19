from django.urls import path
from collections_app import views

urlpatterns = [
    path("", views.collections_list, name="collections_list"),
    path("<int:collection_id>/", views.collection_detail, name="collection_detail"),
]
