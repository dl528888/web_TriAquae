#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    #ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webssh.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
