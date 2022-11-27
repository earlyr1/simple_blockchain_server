import pytest


@pytest.fixture
def balance_payload():
    return {
        "wallet": "0x416a7989a964C9ED60257B064Efc3a30FE6bF2eE",
        "block_num": "0x13371337",
        "network": "avalanche",
    }


@pytest.fixture
def logs_payload():
    return {"block_num": "0x13371337"}
