class UserScopes:
    USER = 'user' # wala tong kaya
    ADMIN = 'admin'
    APPLICATION_ENGR = "ae"
    SALES_ENGR = "se"
    SALES_LEAD = "sl"
    BU_HEAD = "bh"

USER_SCOPE_OPTIONS = [
    (UserScopes.USER, 'user'),
    (UserScopes.ADMIN, 'admin'),
    (UserScopes.APPLICATION_ENGR, 'ae'),
    (UserScopes.SALES_ENGR, 'se'),
    (UserScopes.SALES_LEAD, 'sl'),
    (UserScopes.BU_HEAD, 'bh'),
]