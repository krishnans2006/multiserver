from django.contrib import admin

from .models import Server


# Register your models here.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = (
        "name",
        "repo_url",
        "port",
        "initialized",
        "systemd_applied",
        "nginx_applied",
        "enabled",
    )
    ordering = ("port",)
    save_as = True
    search_fields = ("name", "description", "repo_url", "port", "service_name", "domain_name")
