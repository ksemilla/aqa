class UserScopes:
    USER = 'user' # no permissions
    ADMIN = 'admin' # superuser
    APPLICATION_ENGR = "ae"
    SALES_ENGR = "se"
    SALES_LEAD = "sl"
    BU_HEAD = "bh" #Business Unit Head
    SCM = 'scm' #supply chain personnel

USER_SCOPE_OPTIONS = [
    (UserScopes.USER, 'user'),
    (UserScopes.ADMIN, 'admin'),
    (UserScopes.APPLICATION_ENGR, 'ae'),
    (UserScopes.SALES_ENGR, 'se'),
    (UserScopes.SALES_LEAD, 'sl'),
    (UserScopes.BU_HEAD, 'bh'),
    (UserScopes.SCM, 'scm'),
]