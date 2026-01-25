from web3 import Web3

GANACHE_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    raise Exception("Ganache not running")

DEFAULT_ACCOUNT = w3.eth.accounts[0]
