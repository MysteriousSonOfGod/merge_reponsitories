# coding=utf-8

import hashlib
import json
import time
import requests
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse


class InvalidChainError(Exception):
    def __init__(self, index):
        self.err = f'This chain has been falsified at index {index}'
        Exception.__init__(self, self.err)


class Blockchain:

    def __init__(self):
        self.nodes = set()
        self.chain = []
        self.current_transactions = []
        if not self.chain:
            self.new_block(previous_hash=1, proof=100)

    def new_transaction(self, sender, recipient, amount):
        """
        Create a new Block and adds it to the transactions
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount of the transaction
        :return: <int> The index of the Block which will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index']+1

    def new_block(self, proof, previous_hash=None):
        """
        Adds a new transaction to the list of transactions
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        # Allow the Genesis Block add into Chain without checking
        if previous_hash is not None:
            self.chain.append(block)
        else:
            # Check the Chain
            if self.falsified_checking:
                # Raise a error if received falsified index
                raise InvalidChainError(self.falsified_checking)
            else:
                self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """
        Hash a Block with SHA-256
        :param block: <dict> Block
        :return: <str> SHA_256 string
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Return the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        A simple Work-Proof:
            find a Proof makes the hash of (last_proof, proof) start with three zeros
        :param last_proof: <int> the Proof of last Block
        :return: <int> this Proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Prove if the hash of (last_proof, proof) start with three zeros
        :param last_proof: <str> the Previous Proof
        :param proof: <str> the Current Proof
        :return: <bool> True is correct, False is wrong
        """
        answer = f'{last_proof}{proof}'.encode(encoding='utf-8')
        answer_hash = hashlib.sha256(answer).hexdigest()
        return answer_hash[:5] == '00000'

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url)

    @property
    def falsified_checking(self):
        """
        Check the chain, if any block was falsified, return the index
        :return: <int> or None Index of block
        """
        check_length = len(self.chain) - 1
        while check_length:
            previous_hash = self.chain[check_length]['previous_hash']
            checked_hash = self.hash(self.chain[check_length - 1])
            if previous_hash != checked_hash:
                return check_length - 1
            check_length -= 1
        return None

    def valid_chain(self, chain):
        current_index = 1
        while current_index < len(chain):
            last_block = chain[current_index - 1]
            block = chain[current_index]
            current_index += 1
            print(f'{last_block}')
            print(f'{block}')
            print('-'*20)
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        # We are only looking for chains Longer than ours
        max_length = len(self.chain)
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Check if the length if longer and the chain is valid
                if length < max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

    # def add_block(self, sender, recipient, mount):
    #     """
    #     This is a shortcut to start a transaction and append it into the chain,
    #     similar to method <new_transaction>
    #     """
    #     index = self.new_transaction(sender, recipient, mount)
    #     last_proof = self.last_block['proof']
    #     proof = self.proof_of_work(last_proof)
    #     try:
    #         self.new_block(proof)
    #     except InvalidChainError as e:
    #         print(InvalidChainError.__name__ + ':', e)
    #     else:
    #         print('_'*15)
    #         print('{:<15}'.format(f'index: {index}'))
    #         print('_' * 15)
    #         print('{:<15}'.format(f'proof: {proof}'))
    #         print('_' * 15)
    #         print('{:15}'.format('status: Success'))
    #         print('_' * 15)


# Instantiate a Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifer = str(uuid4()).replace('-', '')
# Instantiate the blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifer,
        amount=1,
    )
    block = blockchain.new_block(proof)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transaction': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    print()
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block{index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain has been replace',
            'new_chain': blockchain.chain,
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'new_chain': blockchain.chain,
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5001)
    # demo = Blockchain()
