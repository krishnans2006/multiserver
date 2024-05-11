from pathlib import Path
import subprocess
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone


def systemd_path(instance, filename):
    return Path("systemd") / f"{instance.service_name}.service"


def nginx_path(instance, filename):
    return Path("nginx") / f"{instance.domain_name}.conf"


# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=255, unique=True)
    service_name = models.CharField(max_length=255, unique=True)
    domain_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=4096)
    repo_url = models.URLField(max_length=255)
    port = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(1024), MaxValueValidator(65535)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    applied_at = models.DateTimeField(null=True, blank=True)

    systemd_file = models.FileField(upload_to=systemd_path)
    systemd_applied = models.BooleanField(default=False)
    nginx_file = models.FileField(upload_to=nginx_path)
    nginx_applied = models.BooleanField(default=False)

    initialized = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)

    def initialize(self):
        if self.initialized:
            return False

        subprocess.run(
            ["git", "clone", self.repo_url, settings.MEDIA_ROOT / "code" / self.service_name]
        )
        subprocess.run(["sudo", "systemctl", "enable", "--now", self.systemd_file.path])
        subprocess.run(
            [
                "sudo",
                "ln",
                "-s",
                self.nginx_file.path,
                f"/etc/nginx/sites-available/{self.domain_name}.conf",
            ]
        )
        subprocess.run(["sudo", "systemctl", "reload", "nginx"])
        self.initialized = True
        self.save()
        return True

    def apply_changes(self):
        if not self.initialized:
            self.initialize()

        changes_made = self.apply_systemd() or self.apply_nginx()
        return changes_made

    def apply_systemd(self):
        if not self.initialized:
            self.initialize()

        if self.systemd_applied:
            return False

        subprocess.run(["sudo", "systemctl", "daemon-reload"])
        subprocess.run(["sudo", "systemctl", "restart", self.systemd_file.path])
        self.systemd_applied = True
        self.applied_at = timezone.now()
        self.save()
        return True

    def apply_nginx(self):
        if not self.initialized:
            self.initialize()

        if self.nginx_applied:
            return False

        subprocess.run(["sudo", "systemctl", "reload", "nginx"])
        self.nginx_applied = True
        self.applied_at = timezone.now()
        self.save()
        return True

    def enable(self):
        if not self.initialized:
            self.initialize()

        if self.enabled:
            return False

        subprocess.run(
            [
                "sudo",
                "ln",
                "-s",
                f"/etc/nginx/sites-available/{self.domain_name}.conf",
                f"/etc/nginx/sites-enabled/{self.domain_name}.conf",
            ]
        )
        subprocess.run(["sudo", "systemctl", "reload", "nginx"])
        self.enabled = True
        self.save()
        return True

    def disable(self):
        if not self.initialized:
            self.initialize()

        if not self.enabled:
            return False

        subprocess.run(["sudo", "rm", f"/etc/nginx/sites-enabled/{self.domain_name}.conf"])
        subprocess.run(["sudo", "systemctl", "reload", "nginx"])
        self.enabled = False
        self.save()
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Server {self.name}>"

    def get_absolute_url(self):
        return reverse("app:detail", kwargs={"id": self.id})
