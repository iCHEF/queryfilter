from __future__ import absolute_import
import django
import os
import sys
from pathlib2 import Path
project_path = Path(__file__).parent.parent.parent/"test_project"
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

django.setup()

