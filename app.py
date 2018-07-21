from flask import Flask,jsonify
from uuid import uuid4
from block_chain import BlockChain
from flask import request
import requests

node_address = uuid4().hex

app = Flask(__name__)

block_chain = BlockChain()

@app.route("/create-transaction",methods = ["POST"])
def create_transaction():
    transaction_data = request.get_json()
    index = block_chain.create_new_transaction(**transaction_data)
    response = {'message' : 'Transaction submitted successfully','block_index' : index}
    return jsonify(response),201

@app.route("/mine",methods = ["POST"])
def mine():
    block  = block_chain.mine_block(node_address)
    response  = {"message"  :"Succssfully mined block",
    "block" : block}
    return jsonify(response),201

@app.route("/chain",methods = ["GET"])
def get_chain():
    print "reached here"
    serialized_chain = block_chain.get_serialized_chain
    response  = {"chain" :serialized_chain}
    return jsonify(response)

@app.route("/register-node" ,methods = ["POST"])
def register_node():
    data = request.get_json()
    block_chain.create_node(data["address"])
    response = {
        'message': 'New node has been added',
        'node_count': len(block_chain.nodes),
        'nodes': list(block_chain.nodes),
    }
    return jsonify(response), 201

@app.route('/sync-chain', methods=['GET'])
def consensus():
    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
       return jsonify({'message': 'No neighbour chain is available'})
    
    longest_chain = max(neighbour_chains, key=len) # Get the longest chain

    if len(block_chain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
        response = {
            'message': 'Chain is already up to date',
            'chain': block_chain.get_serialized_chain
        }
    else:  # If our chain isn't longest, then we store the longest chain
        block_chain.chain = [block_chain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
           'message': 'Chain was replaced',
           'chain': block_chain.get_serialized_chain
        }

    return jsonify(response)

def get_neighbour_chains():
    neighbour_chains = []
    for node_address in block_chain.nodes:
        response = requests.get(node_address+"/chain").json()
        chain = response['chain']
        neighbour_chains.append(chain)
    return neighbour_chains

app.run(debug = True,threaded = True)