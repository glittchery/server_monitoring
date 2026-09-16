import os

from authx import AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"
