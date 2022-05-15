

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("landing", views.landing, name="landing"),
    path("edit/<int:medication_id>", views.edit, name="edit"),
    path("delete/<int:medication_id>", views.delete, name="delete")
]