from flask import Flask, jsonify, request
from HealthPool_functions import *

global WEB3
global CONTRACT_ADDRESS
global CONTRACT_ABI

app = Flask(__name__)


@app.route('/register_participant/<address>/<name>/<int:age>', methods=['GET'])
def register_participant(address, name, age):
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    receipt = writeChain(instance, WEB3.eth.accounts[0], CONTRACT_ADDRESS, "registerParticipant", address, name, age)

    output = [{'receipt': receipt}]

    return jsonify({'result': output})


@app.route('/payfunds_participant/<address>/<int:payment>', methods=['GET'])
def pay_funds(address, payment):
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    receipt = writeChain(instance, address, CONTRACT_ADDRESS, "payFunds", address, payment)

    output = [{'receipt': receipt}]

    return jsonify({'result': output})


@app.route('/total_funds', methods=['GET'])
def total_funds():
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    funds = readChain(instance, CONTRACT_ADDRESS, "getTotalFunds")

    output = [{'total funds': funds}]

    return jsonify({'result': output})


@app.route('/info_participant/<address>', methods=['GET'])
def info_participant(address):
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    info = readChain(instance, CONTRACT_ADDRESS, "getParticipant", address)

    output = [{'address': info[0],
               'id': info[1],
               'name': info[2],
               'age': info[3],
               'funds paid': info[4],
               'last payment': info[5],
               'registered': info[6]}]

    return jsonify({'result': output})


@app.route('/all_info_participant', methods=['GET'])
def all_info_participant():
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    addresses = readChain(instance, CONTRACT_ADDRESS, "getParticipantAddresses")
    output = []

    for a in addresses:
        info = readChain(instance, CONTRACT_ADDRESS, "getParticipant", a)
        output.append({'address': info[0],
                       'id': info[1],
                       'name': info[2],
                       'age': info[3],
                       'funds paid': info[4],
                       'last payment': info[5],
                       'registered': info[6]})

    return jsonify({'result': output})


@app.route('/all_address_participant', methods=['GET'])
def all_address_participant():
    instance = createContractInstance(WEB3, CONTRACT_ABI)
    addresses = readChain(instance, CONTRACT_ADDRESS, "getParticipantAddresses")
    output = [{'addresses': addresses}]

    return jsonify({'result': output})


if __name__ == '__main__':
    WEB3 = connect_to_rpc()
    CONTRACT_ADDRESS = create_contract(WEB3)
    CONTRACT_ABI = get_abi()
    app.run(debug=True)
