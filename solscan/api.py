import logging
from typing import Optional
from .provide import HTTPClient
from .methods import AccountMixin
from .models.public import ChainInfo
from .errors import VersionError
from .errors.network import HTTPRequestError


class Solscan:
    def __new__(cls, version: str, token: str, logger: Optional[logging.Logger] = None):
        logger = logger or logging.getLogger(__name__)
        if version == "public":
            return PublicApi(token, logger)
        elif version == "pro":
            return ProApi(token, logger)
        else:
            raise VersionError()


class PublicApi:
    __client = HTTPClient("https://public-api.solscan.io/")

    def __init__(self, token: str, logger: logging.Logger):
        self.token = token
        self.logger = logger

    async def chain_info(self):
        try:
            json_response = await self.__client.send_request(
                token=self.token, method="chaininfo/"
            )
            return ChainInfo(json_response)
        except HTTPRequestError as e:
            self.logger.error(e, extra="chain_info")
            return None

    async def tools_inspect(self, message: str):
        try:
            params = {"message": message}
            json_response = await self.__client.send_request(
                token=self.token, method="tools/inspect/", params=params
            )
            return json_response
        except HTTPRequestError as e:
            self.logger.error(e, extra="chain_info")
            return None


class ProApi(PublicApi, AccountMixin):
    __host = "https://pro-api.solscan.io/v1.0/"

    def __init__(self, token: str, logger: logging.Logger):
        self.token = token
        self.logger = logger
        self.client = HTTPClient(self.__host)
