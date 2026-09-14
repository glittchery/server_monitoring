from authx import AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = "ZYkHbWinM&5Y6GTC^j$fpN%a!Q7DUi5v"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False

