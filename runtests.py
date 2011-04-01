#!/usr/bin/env python
from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=('django.contrib.admin', 'hollow',),
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    ROOT_URLCONF='hollow.tests.urls',
    SESSION_ENGINE='django.contrib.sessions.backends.file',
)

if __name__ == "__main__":
    call_command('test', 'hollow', traceback=True)
