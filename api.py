from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain
from utils import hash_block, validate_transaction_data

# Instanciar el nodo Flask
app = Flask(__name__)

# Generar una dirección única global para este nodo
node_identifier = str(uuid4()).replace('-', '')

# Instanciar la Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # 1. Ejecutamos el algoritmo de prueba de trabajo
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 2. Recibir recompensa por minar (sender="0" indica que es una moneda nueva)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # 3. Forjamos el nuevo bloque agregándolo a la cadena
    # IMPORTANTE: Usamos hash_block de utils para consistencia
    previous_hash = hash_block(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Nuevo bloque forjado",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # 1. Validamos los datos usando la función auxiliar de utils
    is_valid, message = validate_transaction_data(values)
    
    if not is_valid:
        return jsonify({'message': message}), 400

    # 2. Crear una nueva transacción
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'La transacción se añadirá al Bloque {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return jsonify({'message': "Error: Por favor suministre una lista válida de nodos"}), 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Nuevos nodos han sido añadidos',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Nuestra cadena fue reemplazada',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Nuestra cadena tiene autoridad (es la correcta)',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

# NOTA: No incluimos 'if __name__ == "__main__": app.run()' 
# porque node.py se encarga de ejecutar la aplicación.