import json
import time
import requests
from urllib.parse import urlparse
from utils import hash_block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Crear el bloque génesis
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Añade un nuevo nodo a la lista de nodos.
        :param address: Dirección del nodo. Ej. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('URL inválida')

    def new_block(self, proof, previous_hash=None):
        """
        Crea un nuevo bloque y lo añade a la cadena.
        :param proof: La prueba dada por el algoritmo de Proof of Work
        :param previous_hash: Hash del bloque previo
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or hash_block(self.chain[-1]),
        }

        # Reiniciar las transacciones pendientes
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Crea una nueva transacción para el próximo bloque minado.
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Algoritmo de prueba de trabajo.
        Busca un número p' tal que hash(last_proof, p') tenga 4 ceros al inicio.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Valida la prueba:
        ¿El hash(last_proof, proof) comienza con 0000?
        """
        guess = f"{last_proof}{proof}".encode()

        import hashlib
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def valid_chain(self, chain):
        """
        Determina si una cadena dada es válida.
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # Verificar hash correcto
            if block['previous_hash'] != hash_block(last_block):
                return False

            # Verificar Prueba de Trabajo
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Consenso: reemplazar nuestra cadena por la más larga válida.
        """
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f"http://{node}/chain")

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain

            except requests.exceptions.RequestException:
                continue    # ignorar nodos caídos

        if new_chain:
            self.chain = new_chain
            return True

        return False
