from __future__ import absolute_import
import django
import os
from os.path import dirname, join
import sys
project_path = join(dirname(dirname(dirname(__file__))), "test_project")
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

django.setup()

