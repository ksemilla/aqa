class UserScopes:
    USER = 'user' # wala tong kaya
    ADMIN = 'admin'
    APPLICATION_ENGG = "ae"
    SALES_ENGG = "se"
    SALES_LEAD = "sl"


USER_SCOPE_OPTIONS = [
    (UserScopes.USER, 'user'),
    (UserScopes.ADMIN, 'admin'),
    (UserScopes.APPLICATION_ENGG, 'ae'),
    (UserScopes.SALES_ENGG, 'se'),
    (UserScopes.SALES_LEAD, 'sl'),
]