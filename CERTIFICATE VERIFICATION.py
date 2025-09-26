import hashlib
import json
from time import time
import streamlit as st

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_certificates = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'certificates': self.current_certificates,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_certificates = []
        self.chain.append(block)
        return block

    def new_certificate(self, student_name, course):
        """
        Add a new certificate to the list of certificates
        :param student_name: <str> student's name
        :param course: <str> course name
        :return: <int> index of the block that will hold this certificate
        """
        self.current_certificates.append({
            'student_name': student_name,
            'course': course
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # Hashes a block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number 'proof' such that hash(last_proof + proof) contains 4 leading zeroes
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def verify_certificate(self, student_name):
        """
        Search blockchain for certificates matching student_name
        """
        results = []
        for block in self.chain:
            for cert in block['certificates']:
                if cert['student_name'].lower() == student_name.lower():
                    results.append({
                        'block_index': block['index'],
                        'student_name': cert['student_name'],
                        'course': cert['course'],
                        'block_hash': self.hash(block)
                    })
        return results
