from typing import Dict


class ChainInfo:
    def __init__(self, json_data: Dict[str, int]):
        self.blockHeight: int = json_data.get("blockHeight")
        self.currentEpoch: int = json_data.get("currentEpoch")
        self.absoluteSlot: int = json_data.get("absoluteSlot")
        self.transactionCount: int = json_data.get("transactionCount")

    def __str__(self):
        return f"ChainInfo(blockHeight={self.blockHeight}, currentEpoch={self.currentEpoch}, absoluteSlot={self.absoluteSlot}, transactionCount={self.transactionCount})"
