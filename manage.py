#!/usr/bin/env python
import sys

from django.conf import settings


if __name__ == "__main__":
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'url_tracker',
            'south'
        ],
    )
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
