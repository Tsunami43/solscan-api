from typing import Dict, Any
from io import StringIO
from pandas import read_csv, DataFrame
from ..errors.pro import AccountNotFoundData, ErrorReadResponse


class Account:
    def __init__(self, json_data: Dict[str, Any]):
        self.account: int = json_data.get("account")
        self.lamports: int = json_data.get("lamports")
        if self.lamports is None:
            raise AccountNotFoundData(self.account)
        self.ownerProgram: str = json_data.get("ownerProgram")
        self.type: str = json_data.get("type")
        self.rentEpoch: int = json_data.get("rentEpoch")
        self.executable: bool = json_data.get("executable")

    def __str__(self):
        return f"Account(lamports={self.lamports}, ownerProgram={self.ownerProgram}, type={self.type}, rentEpoch={self.rentEpoch}, executable={self.executable}, account={self.account})"

    def get_sol(self):
        return round(self.lamports / 10**9, 5)


class DataFrameTxs:
    def __init__(self, dataFrame: DataFrame):

        self.dataFrame = dataFrame.rename(columns=lambda x: x.strip()).apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )

    def get_history(self) -> DataFrame:
        # return self.dataFrame[
        #     (self.dataFrame["Type"] == "TokenChange")
        #     & (
        #         (self.dataFrame["ChangeType"] == "inc")
        #         | (self.dataFrame["ChangeType"] == "dec")
        #     )
        #     & (self.dataFrame["TokenName(off-chain)"] != "Wrapped SOL")

        # ]
        return self.dataFrame[
            (
                (self.dataFrame["ChangeType"] == "inc")
                | (self.dataFrame["ChangeType"] == "dec")
            )
            & (self.dataFrame["TokenName(off-chain)"] != "Wrapped SOL")
            & (self.dataFrame["Symbol(off-chain)"] != "WSOL")
            & (self.dataFrame["Symbol(off-chain)"] != "USDC")
            & (self.dataFrame["Symbol(off-chain)"] != "USDT")
        ]

    def to_csv(self, name: str):
        self.dataFrame.to_csv(name + ".csv", index=False)

    @classmethod
    def from_response(cls, response: Any):
        try:
            return cls(read_csv(StringIO(response), usecols=range(12)))
        except Exception as e:
            raise ErrorReadResponse(e)

    def __str__(self):
        return str(self.dataFrame.head(10))
