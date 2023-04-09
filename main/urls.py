from django.urls import path

from . import views

urlpatterns = [
    path("", views.SneakersView.as_view()),
    path("<slug:slug>/", views.SneakerDetailView.as_view(), name="sneaker_detail"),
    path("review/<int:pk>", views.AddReview.as_view(), name="add_review"),
]
