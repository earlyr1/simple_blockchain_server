from collections import defaultdict
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, validator
from pydantic.error_wrappers import ErrorWrapper, ValidationError


class Network(Enum):
    AVALANCHE = 0
    ETHEREUM = 1
    UNKNOWN = -1


network_mapping = defaultdict(lambda: Network.UNKNOWN, {
    'avalanche': Network.AVALANCHE,
    'ethereum': Network.ETHEREUM
})


class BaseModelWithBlockNum(BaseModel):
    block_num: str = Field(example="0xdddd2")

    @validator("block_num", pre=True)
    def val_model(cls, value):
        if value in ["latest", "pending", "earliest"]:
            return value
        if isinstance(value, int):
            return hex(value)
        try:
            _int16 = int(value, 16)
            return hex(_int16)
        except Exception:
            raise ValidationError(
                [ErrorWrapper(ValueError("Block number is not a valid int10, int16 or string"), loc=None)],  # type: ignore
                model=cls,
            )

    def __hash__(self):
        return hash(self.block_num)


class BalancePayload(BaseModelWithBlockNum):
    network: Network = Field(example=Network.AVALANCHE)
    wallet: str = Field(example="0xF3ea77E42F846a")

    @validator("network", pre=True)
    def val_model(cls, value):
        ret = network_mapping[value]
        match ret:
            case Network.UNKNOWN:
                raise ValidationError(
                    [ErrorWrapper(ValueError("Invalid network"), loc=None)],
                    # type: ignore
                    model=cls,
                )
            case _:
                return ret

    def __hash__(self):
        return hash(str(self.network) + ':' + str(self.wallet) + ':' + str(self.block_num))


EventsPayload = BaseModelWithBlockNum


class BalanceResponse(BaseModel):
    balance: int = Field(example=13371337133713371337)


class EventsResponse(BaseModel):
    events: List[dict] = Field(example=[{"from": "foo", "to": "bar"}])


class ErrorResponse(BaseModel):
    error: str = Field(example="Blockchain down ahaha")
