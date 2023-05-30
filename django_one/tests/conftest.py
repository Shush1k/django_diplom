from pathlib import Path

from django.utils.version import get_version

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIRS = ['movies', 'users', 'contact']

assert get_version() >= '4.0.3', 'Пожалуйста, используйте версию Django > 4.0.3'

for app_dir in APP_DIRS:
    if not Path(BASE_DIR / app_dir).is_dir():
        assert False, (
            f'В папке проекта {BASE_DIR} не найдено директории '
            f'приложения {app_dir}'
        )

pytest_plugins = [
    'tests.fixtures.fixture_data',
]
