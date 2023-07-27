from pathlib import Path

from encryption_machine.settings import *

SECRET_KEY='dqsiqisw8zq8j=@ft0=+4kmbc!h@4n_q80+0s8qpp129m'
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
