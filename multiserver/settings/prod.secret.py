DEBUG = False

SECRET_KEY = "django-notinsecure-_+8w#ipp0n7g2nh*#cvq^0%nn6y7)9_ouizr777bmhio#*qa!!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "multiserver",
        "USER": "multiserver",
        "PASSWORD": "multiserver",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

STATIC_ROOT = "/var/www/multiserver/static"
