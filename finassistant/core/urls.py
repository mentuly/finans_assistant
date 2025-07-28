from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("events/", views.events, name="events"),
    path("events/add/", views.add_event, name="add_event"),
    path("events/toggle/<int:event_id>/", views.toggle_event, name="toggle_event"),
    path("transactions/", views.transactions, name="transactions"),
    path("transactions/add/<str:type>/", views.add_transaction, name="add_transaction"),
]