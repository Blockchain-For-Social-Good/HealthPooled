from web3 import Web3, HTTPProvider
import json
from subprocess import Popen, PIPE


def declare_contract():
    return input("Enter the path to your contract (.sol): ")


def connect_to_rpc():
    """Connect to an RPC.
    Enter the ip and port of the rpc when prompted.
    Returns the Web3 objects created from the specified provider.
    """
    provider = "http://"

    ip = input("IP of  provider: ")
    provider += "127.0.0.1" if ip == "" else ip

    provider += ":"

    port = input("Port of provider: ")
    provider += "8545" if port == "" else port

    print("Connecting to provider: " + provider)
    web3 = Web3(HTTPProvider(provider))
    return web3


def initialize_contract(web3, contract_source):
    contract = create_contract(web3, contract_source)

    deployer_address = input("Enter the address of the deployer: ")
    deployer_address = web3.eth.accounts[0] if deployer_address == "" else deployer_address

    gas = input("Enter the desired gas for the contract: ")
    gas = 1000000 if gas == "" else int(gas)

    contract_address = deploy_contract(web3, contract, deployer_address, gas)
    print("The contract address is: " + contract_address)
    return contract_address


def get_contract_bytecode(file_path):
    p = Popen(["solc", "--optimize", "--bin", file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    bytecode, err = p.communicate()

    return "0x" + str(bytecode).split("\\n")[-2]


def get_contract_bytecode_runtime(file_path):
    p = Popen(["solc", "--optimize", "--bin-runtime", file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    bytecode, err = p.communicate()

    return "0x" + str(bytecode).split("\\n")[-2]


def get_contract_abi(file_path):
    p = Popen(["solc", "--optimize", "--abi", file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    abi, err = p.communicate()

    return json.loads(str(abi).split("\\n")[-2])


def create_contract(web3, file_path):
    return web3.eth.contract(abi=get_contract_abi(file_path),
                             bytecode=get_contract_bytecode(file_path),
                             bytecode_runtime=get_contract_bytecode_runtime(file_path))


def deploy_contract(web3, contract, deployer_address, gas):
        tx_hash = contract.deploy(transaction={"from": deployer_address, "gas": gas})
        receipt = web3.eth.getTransactionReceipt(tx_hash)
        return receipt["contractAddress"]


def create_contract_instance(web3, abi):
    return web3.eth.contract(abi=abi)


def read_chain(contract_instance, contract_address, function_name, *args):

    contract_call = contract_instance.call({"to": contract_address})

    if function_name == "getTotalFunds":
        return contract_call.getTotalFunds()
    if function_name == "getParticipantAddresses":
        return contract_call.getParticipantAddresses()
    if function_name == "getParticipant":
        return contract_call.getParticipant(args[0])


def write_chain(contract_instance, from_address, contract_address, function_name, *args):

    contract_transact = contract_instance.transact({"from": from_address, "to": contract_address, "gas": 1000000})

    if function_name == "registerParticipant":
        return contract_transact.registerParticipant(args[0], args[1], args[2])
    if function_name == "payFunds":
        return contract_transact.payFunds(args[0], args[1])
