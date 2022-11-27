import logging
from typing import Union

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from web3 import Web3
from web3.datastructures import MutableAttributeDict

from bc_server.models import (
    BalancePayload,
    BalanceResponse,
    ErrorResponse,
    EventsPayload,
    EventsResponse,
    Network,
)
from bc_server.web3_client import AsyncAvalancheAPI, AsyncEthAPI
from bc_server.settings import settings

info_router = APIRouter(prefix="/info")


@info_router.post(
    "/balance",
    responses={
        200: {"model": BalanceResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
#@lru_cache(maxsize=128)
async def balance(payload: BalancePayload) -> Union[BalanceResponse, JSONResponse]:
    try:
        kwargs = {
            "account": Web3.toChecksumAddress(payload.wallet),
            "block_identifier": payload.block_num,
        }
        match payload.network:
            case Network.AVALANCHE:
                resp = await AsyncAvalancheAPI.eth.get_balance(**kwargs)
            case Network.ETHEREUM:
                resp = await AsyncEthAPI.eth.get_balance(**kwargs)
    except ValueError as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(error=str(e)).dict(),
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(error=str(e)).dict(),
        )
    return BalanceResponse(balance=resp)


@info_router.post(
    "/events",
    responses={
        200: {"model": EventsResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
#@lru_cache(maxsize=128)
async def events(
    payload: EventsPayload,
) -> Union[EventsResponse, JSONResponse]:  # found no async contract api in web3.py
    try:
        logs = await AsyncAvalancheAPI.eth.get_logs(
            {"fromBlock": payload.block_num, "address": settings.CONTRACT_ID}
        )
    except ValueError as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(error=str(e)).dict(),
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(error=str(e)).dict(),
        )
    # converting all HexBytes to str '0x...'
    try:
        for idx, log in enumerate(logs):
            mut_log = MutableAttributeDict(log)
            mut_log.blockHash = log.blockHash.hex()
            mut_log.transactionHash = log.transactionHash.hex()
            for t_idx, t in enumerate(log.topics):
                mut_log.topics[t_idx] = t.hex()
            logs[idx] = mut_log
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(error=str(e)).dict(),
        )

    return EventsResponse(events=logs)
