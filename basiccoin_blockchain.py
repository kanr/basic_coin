
#simple blockchain written in python
import datetime as datetime
import hashlib as hasher
from flask import Flask
from flask import request
import json
node = Flask(__name__)

# each block on the chain will have a self identifying hash, block index, timestamp, data and previous previous_hash
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode())
        return sha.hexdigest()

"""    def __str__(self):
        output = str(self.index) + " / " + \
            str(self.timestamp) + " / " + \
            str(self.data) + " / " + \
            str(self.previous_hash[:10])
        return output
"""

def create_genesis_block():
    return Block(0, datetime.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
    }, "0")

miner_address = "2ranpdme2d-random-miner-address-z0m3c621dqm"
# this nodes blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
#store the transactions that this node has in a list
this_nodes_transactions = []
#Store the url of every peer in the network for communication
peer_nodes = []
mining = True


@node.route('/txion', methods=['POST'])
def transaction():
    #on each new POST request we extract the transaction data
    new_txion = request.get_json()
    this_nodes_transactions.append(new_txion)
    print("New transaction")
    print("From {}".format(new_txion['from'].encode('ascii','replace')))
    print("To: {}".format(new_txion['to'].encode('ascii','replace')))
    print("Amount: {}\n".format(new_txion['amount']))
    #Then we let the know it worked out
    return("Transaction sumbession successful\n")

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    #convert our blocks into dictionaries so we can send them as json objects
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        chain_to_send[i] = {
        "index": block_index,
        "timestamp": block_timestamp,
        "data": block_data,
        "hash": block_hash
        }
        chain_to_send = json.dumps(chains_to_send)
        return chain_to_send

def find_new_chains():
    # Get the blockchains of every other nodes
    other_chains = []
    for node_url in peer_nodes:
        # get their chains using a GET request
        block = requests.get(node_url + "/blocks").content
        # Convert the JSON object to a python dictionary
        block = json.loads(block)
    return other_chains

def consensus():
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chains isn't the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    #if the longest chain isn't ours the we stop mining and set our chain to the longest None
    blockchain = longest_chain

def proof_of_work(last_proof):
    #create a variable that we will use to find our next prrof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until it's eqal to a number divisible by 9 and the proof of work of the previous block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found we can return it as a proof of our work
    return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    # Get the last proof of work
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    #find the proof of work for the current block being mined
    #Note: the program will hang here until a new proof of work is found
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
    {"from": "network", "to": miner_address, "amount": 1}
    )
    # Now we can gather the data needed to create the new block
    new_block_data = {
    "proof-of-work" : proof,
    "transactions" : list(this_nodes_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = datetime.datetime.now()
    last_block_hash = last_block.hash
    # empty transaction list
    this_nodes_transaction[:] = []
    #now create the new block
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        new_block_hash
    )
    blockchain.append(mined_block)
    # Let the client know we mined a blocks
    return json.dumps ({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"

    node.run()
