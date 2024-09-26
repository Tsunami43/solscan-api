from .base import SolscanError


class AccountNotFoundData(SolscanError):
    def __init__(self, account: str):
        self.message = f"Account({account}) not found data"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ErrorReadResponse(SolscanError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def get(self, account: str):
        return f"ErrorReadResponse ({account}): {self.message}"

    def __str__(self):
        return f"ErrorReadResponse: {self.message}"
