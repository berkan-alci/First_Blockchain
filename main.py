from blockchain import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()


@app.route('/mine-block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)

    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)

    response = {'message': 'Congrats, you mined a block',
                'index': block['index'],
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

    response = {'is_valid': is_valid,
                'message': 'Chain has been successfully validated!'}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
