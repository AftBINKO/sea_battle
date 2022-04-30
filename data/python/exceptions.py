class NotAuthorizedError(Exception):
    pass


class NotLicensedError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class NoLauncherRunError(Exception):
    pass