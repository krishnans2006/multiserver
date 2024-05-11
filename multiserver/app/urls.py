from django.urls import path

from . import views


urlpatterns = [
    path("", views.ServerListView.as_view(), name="list"),
    path("create/", views.ServerCreateView.as_view(), name="create"),
    path("<int:server_id>/", views.ServerDetailView.as_view(), name="detail"),
    path("<int:server_id>/update/", views.ServerUpdateView.as_view(), name="update"),
    path("<int:server_id>/delete/", views.ServerDeleteView.as_view(), name="delete"),
    path("<int:server_id>/initialize/", views.initialize_view, name="initialize"),
    path("<int:server_id>/apply-nginx/", views.apply_nginx_view, name="apply_nginx"),
    path("<int:server_id>/apply-systemd/", views.apply_systemd_view, name="apply_systemd"),
    path("<int:server_id>/apply/", views.apply_all_view, name="apply_all"),
    path("<int:server_id>/enable/", views.enable_view, name="enable"),
    path("<int:server_id>/disable/", views.disable_view, name="disable"),
]
