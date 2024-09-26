from datetime import datetime
from typing import Union
from ..models.account import Account, DataFrameTxs
from ..errors.pro import AccountNotFoundData, ErrorReadResponse
from ..errors.network import HTTPRequestError


class AccountMixin:
    __block = "account/"

    async def get_account(self, account: str):
        try:
            json_response = await self.client.send_request(
                token=self.token, method=self.__block + account
            )

            output = Account(json_response)
            self.logger.info(f"Success(account={account})", extra="get_account")
            return output
        except AccountNotFoundData as e:
            self.logger.error(e, extra="get_account")
            return None

        except HTTPRequestError as e:
            self.logger.error(e, extra="get_account")
            return None

    async def export_transactions(
        self,
        account: str,
        _type: Union["all", "tokenchange", "soltransfer"] = "all",
        fromTime: int = 0,
        toTime: int = None,
    ):
        if toTime is None:
            toTime = int(datetime.now().timestamp())

        params = {
            "account": account,
            "type": _type,
            "fromTime": fromTime,
            "toTime": toTime,
        }
        try:
            response = await self.client.send_request(
                token=self.token,
                method=self.__block + "exportTransactions",
                params=params,
            )

            output = DataFrameTxs.from_response(response)
            self.logger.info(f"Success(param={params})", extra="export_transactions")
            return output
        except ErrorReadResponse as e:
            self.logger.error(e.get(account), extra="export_transactions")
            return None

        except HTTPRequestError as e:
            self.logger.error(e, extra="export_transactions")
            return None
