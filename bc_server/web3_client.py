from web3 import Web3
from web3.eth import AsyncEth

from bc_server.settings import settings

ETH_URL = "https://rpc.ankr.com/eth"
AVL_URL = "https://rpc.ankr.com/avalanche"


AsyncAvalancheAPI = Web3(
    Web3.AsyncHTTPProvider(AVL_URL), modules={"eth": (AsyncEth,)}, middlewares=[]
)
AsyncEthAPI = Web3(
    Web3.AsyncHTTPProvider(ETH_URL), modules={"eth": (AsyncEth,)}, middlewares=[]
)
