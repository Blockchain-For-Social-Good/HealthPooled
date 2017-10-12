from flask import Flask, jsonify, request
from HealthPool_functions import *

global CONTRACT_SOURCE
global WEB3
global CONTRACT_ADDRESS
global CONTRACT_ABI

app = Flask(__name__)


@app.route('/participants', methods=['POST'])
def register_participant():
    """
    :return: json including the transaction hash and the participant data
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)

    receipt = write_chain(instance, WEB3.eth.accounts[0], CONTRACT_ADDRESS, "registerParticipant", request.json['address'], request.json['name'], request.json['age'])
    participant = read_chain(instance, CONTRACT_ADDRESS, "getParticipant", request.json['address'])

    participant_dict = {'address': participant[0],
               'id': participant[1],
               'name': participant[2],
               'age': participant[3],
               'funds paid': participant[4],
               'last payment': participant[5],
               'registered': participant[6]}

    output = [{'transaction': receipt,
               'participant': participant_dict}]

    return jsonify({'result': output})


@app.route('/participants/<address>/funds', methods=['PUT'])
def pay_funds(address):
    """
    :param address: Ethereum address of a registered participant
    :return: json of the transaction hash and the updated participant data
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)
    receipt = write_chain(instance, address, CONTRACT_ADDRESS, "payFunds", address, request.json['payment'])
    participant = read_chain(instance, CONTRACT_ADDRESS, "getParticipant", address)

    participant_dict = {'address': participant[0],
               'id': participant[1],
               'name': participant[2],
               'age': participant[3],
               'funds paid': participant[4],
               'last payment': participant[5],
               'registered': participant[6]}

    output = [{'transaction': receipt,
               'participant': participant_dict}]

    return jsonify({'result': output})


@app.route('/total_funds', methods=['GET'])
def total_funds():
    """
    :return: json of the total funds in the health pool
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)
    funds = read_chain(instance, CONTRACT_ADDRESS, "getTotalFunds")

    output = [{'total funds': funds}]

    return jsonify({'result': output})


@app.route('/participants/<address>', methods=['GET'])
def info_participant(address):
    """
    :param address: Ethereum address of a registered participant
    :return: json of the specified participant's data
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)
    info = read_chain(instance, CONTRACT_ADDRESS, "getParticipant", address)

    output = [{'address': info[0],
               'id': info[1],
               'name': info[2],
               'age': info[3],
               'funds paid': info[4],
               'last payment': info[5],
               'registered': info[6]}]

    return jsonify({'result': output})


@app.route('/participants', methods=['GET'])
def all_info_participant():
    """
    :return: json of all of the participants in the health pool
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)
    addresses = read_chain(instance, CONTRACT_ADDRESS, "getParticipantAddresses")
    output = []

    for a in addresses:
        info = read_chain(instance, CONTRACT_ADDRESS, "getParticipant", a)
        output.append({'address': info[0],
                       'id': info[1],
                       'name': info[2],
                       'age': info[3],
                       'funds paid': info[4],
                       'last payment': info[5],
                       'registered': info[6]})

    return jsonify({'result': output})


@app.route('/participants/addresses', methods=['GET'])
def all_address_participant():
    """
    :return: json that includes a list of all of the participant addresses
    """
    instance = create_contract_instance(WEB3, CONTRACT_ABI)
    addresses = read_chain(instance, CONTRACT_ADDRESS, "getParticipantAddresses")
    output = [{'addresses': addresses}]

    return jsonify({'result': output})


if __name__ == '__main__':
    WEB3 = connect_to_rpc()
    CONTRACT_SOURCE = declare_contract()
    CONTRACT_ADDRESS = initialize_contract(WEB3, CONTRACT_SOURCE)
    CONTRACT_ABI = get_contract_abi(CONTRACT_SOURCE)
    app.run(debug=True)
