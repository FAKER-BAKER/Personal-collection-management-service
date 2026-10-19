from django.urls import path
from items_app import views

urlpatterns = [
    path("", views.items_list, name="items_list"),
    path("<int:item_id>/", views.item_detail, name="item_detail"),
]
