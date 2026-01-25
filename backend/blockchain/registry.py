from .web3_client import w3, DEFAULT_ACCOUNT

CONTRACT_ADDRESS = "0x1BcD95c05584bdedbBACC55D1bc5Cbd24Ba5B844"

CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "hash", "type": "bytes32"}],
        "name": "issue",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "hash", "type": "bytes32"}],
        "name": "revoke",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "issued",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "revoked",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "hash", "type": "bytes32"}],
        "name": "verify",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=CONTRACT_ABI
)

def issue_hash(hash_hex: str):
    return contract.functions.issue(
        bytes.fromhex(hash_hex)
    ).transact({"from": DEFAULT_ACCOUNT})

def verify_hash(hash_hex: str) -> bool:
    return contract.functions.verify(
        bytes.fromhex(hash_hex)
    ).call()

def revoke_hash(hash_hex: str):
    return contract.functions.revoke(
        bytes.fromhex(hash_hex)
    ).transact({"from": DEFAULT_ACCOUNT})
