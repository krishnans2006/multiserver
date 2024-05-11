from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Server
from django.contrib import messages


# Create your views here.
class ServerListView(ListView):
    context_object_name = "servers"
    model = Server
    ordering = ["port"]


class ServerDetailView(DetailView):
    context_object_name = "server"
    model = Server
    pk_url_kwarg = "server_id"


class ServerCreateView(CreateView):
    context_object_name = "server"
    extra_context = {"title": "Create Server"}
    fields = [
        "name",
        "description",
        "repo_url",
        "port",
        "service_name",
        "systemd_file",
        "domain_name",
        "nginx_file",
    ]
    model = Server
    pk_url_kwarg = "server_id"
    template_name = "obj_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("app:detail", kwargs={"server_id": self.object.id})


class ServerUpdateView(UpdateView):
    context_object_name = "server"
    extra_context = {"title": "Update Server"}
    fields = [
        "name",
        "description",
        "repo_url",
        "port",
        "service_name",
        "systemd_file",
        "domain_name",
        "nginx_file",
    ]
    model = Server
    pk_url_kwarg = "server_id"
    template_name = "obj_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("app:detail", kwargs={"server_id": self.object.id})


class ServerDeleteView(DeleteView):
    context_object_name = "server"
    extra_context = {"title": "Delete Server"}
    model = Server
    pk_url_kwarg = "server_id"
    template_name = "obj_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse_lazy("app:list")


def initialize_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.initialize()
        messages.success(request, f"{server.name} initialized.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Initialize Server",
        "message": f"initialize <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)


def apply_systemd_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.apply_systemd()
        messages.success(request, f"Systemd config applied for {server.name}.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Apply systemd",
        "message": f"update systemd config for <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)


def apply_nginx_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.apply_nginx()
        messages.success(request, f"Nginx config applied for {server.name}.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Apply nginx",
        "message": f"update nginx config for <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)


def apply_all_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.apply_changes()
        messages.success(request, f"Configs applied for {server.name}.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Apply All",
        "message": f"update all configs for <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)


def enable_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.enable()
        messages.success(request, f"{server.name} enabled.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Enable Server",
        "message": f"enable <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)


def disable_view(request: HttpRequest, server_id: int) -> HttpResponse:
    server = get_object_or_404(Server, id=server_id)

    if request.method == "POST":
        server.disable()
        messages.success(request, f"{server.name} disabled.")
        return redirect("app:detail", server_id=server.id)

    context = {
        "title": "Disable Server",
        "message": f"disable <strong>{server.name}</strong>",
        "back": reverse_lazy("app:detail", kwargs={"server_id": server.id}),
    }

    return render(request, "confirm.html", context)
