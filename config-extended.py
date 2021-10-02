#  Nikulin Vasily © 2021
################
# Flask-Security
################

# URLs
SECURITY_URL_PREFIX = "/admin"
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Включает регистрацию
SECURITY_REGISTERABLE = True
SECURITY_REGISTER_URL = "/register/"
SECURITY_SEND_REGISTER_EMAIL = False

# Включает сброс пароля
SECURITY_RECOVERABLE = True
SECURITY_RESET_URL = "/reset/"
SECURITY_SEND_PASSWORD_RESET_EMAIL = True

# Включает изменение пароля
SECURITY_CHANGEABLE = True
SECURITY_CHANGE_URL = "/change/"
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

SECURITY_PASSWORD_SALT = 'gg'
