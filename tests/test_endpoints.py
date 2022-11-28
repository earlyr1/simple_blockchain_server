import pytest

from httpx import AsyncClient
from pytest_mock import MockerFixture
from web3.datastructures import AttributeDict
from hexbytes import HexBytes

from bc_server.main import app

pytestmark = [
    pytest.mark.usefixtures("balance_payload", "logs_payload"),
    pytest.mark.asyncio,
]


class TestGetBalance:
    endpoint = "/info/balance"

    async def test_all_ok(self, balance_payload, mocker: MockerFixture):
        mocker.patch(
            "bc_server.web3_client.AsyncAvalancheAPI.eth.get_balance",
            return_value=13371337,
        )
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json=balance_payload)
        assert response.status_code == 200
        assert response.json() == {"balance": 13371337}

    async def test_missing_field(self, balance_payload):
        del balance_payload["wallet"]
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json=balance_payload)
        assert response.status_code == 400
        assert response.json() == {
            "error": "Wasn't able to validate your message: 1 validation error for "
            "Request\n"
            "body -> wallet\n  "
            "field required (type=value_error.missing)"
        }

    async def test_blockchain_api_fail(self, balance_payload, mocker: MockerFixture):
        mocker.patch(
            "bc_server.web3_client.AsyncAvalancheAPI.eth.get_balance",
            side_effect=Exception("Oh no"),
        )
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json=balance_payload)
        assert response.status_code == 500
        assert response.json() == {"error": "Oh no"}


class TestGetLogs:
    endpoint = "/info/events"

    async def test_all_ok(self, logs_payload, mocker: MockerFixture):
        mocker.patch(
            "bc_server.web3_client.AsyncAvalancheAPI.eth.get_logs",
            return_value=[
                AttributeDict(
                    {
                        "address": "0x66357dCaCe80431aee0A7507e2E361B7e2402370",
                        "topics": [
                            HexBytes(
                                "0x54787c404bb33c88e86f4baf88183a3b0141d0a848e6a9f7a13b66ae3a9b73d1"
                            ),
                            HexBytes(
                                "0x000000000000000000000000156264794f66141c92e839c712b21d0a222a6147"
                            ),
                            HexBytes(
                                "0x000000000000000000000000156264794f66141c92e839c712b21d0a222a6147"
                            ),
                        ],
                        "data": "0x000000000000000000000000b97ef9ef8734c71904d8002f8b6bc66dd9c48a6e000000000000000000000000a7d7079b0fead91f3e65f86e8915cb59c1a4c66400000000000000000000000000000000000000000000000000000000b2d31f0000000000000000000000000000000000000000000000000000000000b2cddcda",
                        "blockNumber": 22910051,
                        "transactionHash": HexBytes(
                            "0x0abcb7282373198c0b2c0c6bf1f181dc56026cf4b30ffc6403a94f055b5ca57d"
                        ),
                        "transactionIndex": 2,
                        "blockHash": HexBytes(
                            "0xf90224ae8f874bdb517184d36be695c53eff12151e6516e46656573d15fbd2dc"
                        ),
                        "logIndex": 13,
                        "removed": False,
                    }
                ),
                AttributeDict(
                    {
                        "address": "0x66357dCaCe80431aee0A7507e2E361B7e2402370",
                        "topics": [
                            HexBytes(
                                "0x54787c404bb33c88e86f4baf88183a3b0141d0a848e6a9f7a13b66ae3a9b73d1"
                            ),
                            HexBytes(
                                "0x000000000000000000000000d41b24bba51fac0e4827b6f94c0d6ddeb183cd64"
                            ),
                            HexBytes(
                                "0x000000000000000000000000d41b24bba51fac0e4827b6f94c0d6ddeb183cd64"
                            ),
                        ],
                        "data": "0x000000000000000000000000a7d7079b0fead91f3e65f86e8915cb59c1a4c664000000000000000000000000c7198437980c041c805a1edcba50c1ce5db95118000000000000000000000000000000000000000000000000000000002e16b0ae000000000000000000000000000000000000000000000000000000002e1d7f95",
                        "blockNumber": 22910163,
                        "transactionHash": HexBytes(
                            "0x0632753fc3a2dea553a7d8bb8cda7675dbdbdff99477afef7281c5033b919862"
                        ),
                        "transactionIndex": 1,
                        "blockHash": HexBytes(
                            "0x1348da6037fad050d1b44da06b804eaec869a555665668b6139457746c164eb7"
                        ),
                        "logIndex": 11,
                        "removed": False,
                    }
                ),
            ],
        )
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json=logs_payload)
        assert response.status_code == 200
        assert response.json() == {
            "events": [
                {
                    "address": "0x66357dCaCe80431aee0A7507e2E361B7e2402370",
                    "blockHash": "0xf90224ae8f874bdb517184d36be695c53eff12151e6516e46656573d15fbd2dc",
                    "blockNumber": 22910051,
                    "data": "0x000000000000000000000000b97ef9ef8734c71904d8002f8b6bc66dd9c48a6e000000000000000000000000a7d7079b0fead91f3e65f86e8915cb59c1a4c66400000000000000000000000000000000000000000000000000000000b2d31f0000000000000000000000000000000000000000000000000000000000b2cddcda",
                    "logIndex": 13,
                    "removed": False,
                    "topics": [
                        "0x54787c404bb33c88e86f4baf88183a3b0141d0a848e6a9f7a13b66ae3a9b73d1",
                        "0x000000000000000000000000156264794f66141c92e839c712b21d0a222a6147",
                        "0x000000000000000000000000156264794f66141c92e839c712b21d0a222a6147",
                    ],
                    "transactionHash": "0x0abcb7282373198c0b2c0c6bf1f181dc56026cf4b30ffc6403a94f055b5ca57d",
                    "transactionIndex": 2,
                },
                {
                    "address": "0x66357dCaCe80431aee0A7507e2E361B7e2402370",
                    "blockHash": "0x1348da6037fad050d1b44da06b804eaec869a555665668b6139457746c164eb7",
                    "blockNumber": 22910163,
                    "data": "0x000000000000000000000000a7d7079b0fead91f3e65f86e8915cb59c1a4c664000000000000000000000000c7198437980c041c805a1edcba50c1ce5db95118000000000000000000000000000000000000000000000000000000002e16b0ae000000000000000000000000000000000000000000000000000000002e1d7f95",
                    "logIndex": 11,
                    "removed": False,
                    "topics": [
                        "0x54787c404bb33c88e86f4baf88183a3b0141d0a848e6a9f7a13b66ae3a9b73d1",
                        "0x000000000000000000000000d41b24bba51fac0e4827b6f94c0d6ddeb183cd64",
                        "0x000000000000000000000000d41b24bba51fac0e4827b6f94c0d6ddeb183cd64",
                    ],
                    "transactionHash": "0x0632753fc3a2dea553a7d8bb8cda7675dbdbdff99477afef7281c5033b919862",
                    "transactionIndex": 1,
                },
            ]
        }

    async def test_missing_block_num(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json={})
        assert response.status_code == 400
        assert response.json() == {'error': "Wasn't able to validate your message: 1 validation error for "
            'Request\n'
            'body -> block_num\n'
            '  field required (type=value_error.missing)'
        }

    async def test_blockchain_error(self, logs_payload, mocker: MockerFixture):
        mocker.patch("bc_server.web3_client.AsyncAvalancheAPI.eth.get_logs", side_effect=Exception("Oh my"))
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(self.endpoint, json=logs_payload)
        assert response.status_code == 404
        assert response.json() == {'error': 'Oh my'}
