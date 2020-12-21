import os
import string

import django
from django.test import TestCase

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_edu.settings.develop")
django.setup()

from django_redis import get_redis_connection

redis_connection = get_redis_connection('default')
