import json
from uuid import uuid4
from blockchain.blockchain import Blockchain
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()

# address on port 5000
node_address = str(uuid4()).replace('-', '')


@app.route('/mine-block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)

    prev_hash = blockchain.hash(prev_block)
    blockchain.add_transaction(
        sender=node_address, recipient='Berkan', amount=1)
    block = blockchain.create_block(proof, prev_hash)

    response = {'message': 'Congrats, you mined a block',
                'index': block['index'],
                'transactions': block['transactions'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']
                }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_blockchain():
    response = {'chain': blockchain.chain,
                'length_chain': len(blockchain.chain)
                }
    return jsonify(response), 200


@app.route('/is-valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {'message': 'Blockchain is valid',
                    'is_valid': is_valid, }
    else:
        response = {'message': 'Blockchain is NOT valid',
                    'is_valid': is_valid, }

    return jsonify(response), 200


@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()

    transaction_keys = ['sender', 'recipient', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Keys in transaction are missing', 400

    i = blockchain.add_transaction(
        json['sender'], json['recipient'], json['amount'])
    response = {'message': f' This transaction will be added to Block: {i}'}
    return jsonify(response), 201


@app.route('/connect-node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        return 'No node', 400

    for node in nodes:
        blockchain.add_node(node)

    response = {'message': 'Nodes connected to BerkieCoin Network',
                'total_nodes': list(blockchain.nodes)}

    return jsonify(response), 201


@app.route('/replace-chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()

    if is_chain_replaced:
        response = {'message': 'Chain has been replaced by the longest one',
                    'new_chain': blockchain.chain, }
    else:
        response = {'message': "Chain has NOT been replaced since it's the longest one",
                    'chain': blockchain.chain, }
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
