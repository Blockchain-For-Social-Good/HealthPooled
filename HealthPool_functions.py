from web3 import Web3, HTTPProvider
import json
from subprocess import Popen, PIPE


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


def create_contract(web3):
    contract = createContract(web3, 'HealthPool.sol')
    contract_address = deployContract(web3, contract,web3.eth.accounts[0],1000000)
    print("The contract address is: " + contract_address)
    return contract_address


def get_abi():
    contract_abi = getContractAbi('HealthPool.sol')
    return contract_abi


def getContractBytecode(filePath):
    p = Popen(["solc","--optimize","--bin",filePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    bytecode, err = p.communicate()

    return "0x" + str(bytecode).split("\\n")[-2]


def getContractBytecodeRuntime(filePath):
    p = Popen(["solc","--optimize","--bin-runtime",filePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    bytecode, err = p.communicate()

    return "0x" + str(bytecode).split("\\n")[-2]


def getContractAbi(filePath):
    p = Popen(["solc","--optimize","--abi",filePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    abi, err = p.communicate()

    return json.loads(str(abi).split("\\n")[-2])

def createContract(web3, filePath):
    return web3.eth.contract(abi=getContractAbi(filePath), bytecode=getContractBytecode(filePath), bytecode_runtime=getContractBytecodeRuntime(filePath))

#returns transaction receipt
def deployContract(web3, contract, deployer_address, gas):
        tx_hash = contract.deploy(transaction={"from":deployer_address,"gas":gas})
        #attribute dict
        receipt = web3.eth.getTransactionReceipt(tx_hash)
        return receipt["contractAddress"]

def createContractInstance(web3, abi):
    return web3.eth.contract(abi=abi)

def readChain(contract_instance, contractaddr, function_name, *args):

    contract_call = contract_instance.call({"to":contractaddr})

    if function_name == "getTotalFunds":
        return contract_call.getTotalFunds()
    if function_name == "getParticipantAddresses":
        return contract_call.getParticipantAddresses()
    if function_name == "getParticipant":
        return contract_call.getParticipant(args[0])

def writeChain(contract_instance, fromaddr, contractaddr, function_name, *args):

    contract_transact = contract_instance.transact({"from":fromaddr, "to":contractaddr, "gas":1000000})

    if function_name == "registerParticipant":
        return contract_transact.registerParticipant(args[0],args[1],args[2])
    if function_name == "payFunds":
        return contract_transact.payFunds(args[0],args[1])