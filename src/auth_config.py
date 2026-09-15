from authx import AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = "***"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_COOKIE_SECURE = False

