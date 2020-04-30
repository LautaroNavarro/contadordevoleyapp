import subprocess
import os


def pytest_configure():
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'api.testing_settings':
        subprocess.Popen(
            "python3 manage.py makemigrations --settings=api.testing_settings".split(),
            stdout=subprocess.PIPE,
        ).communicate()
        subprocess.Popen(
            "python3 manage.py migrate --settings=api.testing_settings".split(),
            stdout=subprocess.PIPE,
        ).communicate()
