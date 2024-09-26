class SolscanError(Exception):
    """Base class for errors in Solscan API."""

    pass


class VersionError(SolscanError):
    """Error raised when an invalid API version is specified."""

    def __init__(self):
        self.message = "Invalid version for Solscan; available versions: public or pro"
        super().__init__(self.message)
