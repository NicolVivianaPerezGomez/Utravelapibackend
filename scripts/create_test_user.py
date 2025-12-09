import os
import sys
import pathlib
import django

# Ensure project root is on sys.path so `apiutravel` package is importable
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apiutravel.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if User.objects.filter(username='apitest').exists():
    print('exists')
else:
    User.objects.create_user('apitest', 'apitest@example.com', 'TestPass123!')
    print('created')
