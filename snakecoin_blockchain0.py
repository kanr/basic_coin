
#simple blockchain written in python
import datetime as datetime
import hashlib as hasher
from snakecoin_block import *
from flask import flask
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

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data = "I'm block" + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


# create the blockchain and add the genesis block.
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blcoks to add after the genesis block?
num_of_blocks_to_add = 2

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
     block_to_add = next_block(previous_block)
     blockchain.append(block_to_add)
     previous_block = block_to_add

     print ("block #{} has been added to the blockchain!".format(block_to_add.index))
     print ("Hash: {}\n".format(block_to_add.hash))
