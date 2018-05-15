from __future__ import absolute_import
import django
import os
import sys
from os.path import dirname, join

project_path = join(dirname(dirname(dirname(__file__))), "test_project")

sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

django.setup()
