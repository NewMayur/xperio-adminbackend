# Other modules
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(ENV_FILE_PATH)
# Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
# Ratelimit
RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED") == "True"
RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI")
# Caching
CACHE_TYPE = os.environ.get("CACHE_TYPE")
CACHE_ENABLED = os.environ.get("CACHE_ENABLED") == "True"
CACHE_STORAGE_URL = os.environ.get("CACHE_STORAGE_URL", None)
CACHE_EXEMPTED_ROUTES = [
    "/api/auth/",
]
IMAGE_URL = os.environ.get("IMAGE_URL")
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY",
)


class DevConfig:
    # Flask
    TESTING = True
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    STATIC_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = SECRET_KEY
    # Database
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    # Ratelimit
    RATELIMIT_ENABLED = RATELIMIT_ENABLED
    RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI
    RATELIMIT_STRATEGY = "fixed-window"  # or "moving-window"
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = True
    RATELIMIT_HEADERS_ENABLED = True
    # Caching
    CACHE_ENABLED = CACHE_ENABLED
    CACHE_TYPE = CACHE_TYPE
    CACHE_KEY_PREFIX = "flask_cache_"
    CACHE_EXEMPTED_ROUTES = CACHE_EXEMPTED_ROUTES
    if CACHE_TYPE != "SimpleCache" and CACHE_STORAGE_URL:
        CACHE_REDIS_URL = CACHE_STORAGE_URL
        CACHE_DEFAULT_TIMEOUT = 180
    else:
        CACHE_DEFAULT_TIMEOUT = 60
    IMAGE_URL = IMAGE_URL
    JWT_SECRET_KEY = JWT_SECRET_KEY
