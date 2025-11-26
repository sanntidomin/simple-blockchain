import hashlib
import json

def hash_block(block):
    """
    Crea un hash SHA-256 de un bloque.
    :param block: <dict> Bloque
    :return: <str> Hash en hexadecimal
    """
    # Nos aseguramos de que el diccionario esté ordenado (sort_keys=True)
    # De lo contrario, hashes inconsistentes romperían la cadena.
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def validate_transaction_data(data):
    """
    Valida que los datos de una transacción entrante sean correctos.
    :param data: <dict> Datos recibidos por POST
    :return: (Boolean, String) -> (Es_Valido, Mensaje_Error)
    """
    required = ['sender', 'recipient', 'amount']

    # 1. Verificar que existen las claves
    if not all(k in data for k in required):
        return False, "Faltan datos requeridos (sender, recipient, amount)"

    # 2. Verificar que el monto sea un número y mayor a 0
    if not isinstance(data['amount'], (int, float)):
        return False, "El monto (amount) debe ser numérico"
    
    if data['amount'] <= 0:
        return False, "El monto debe ser mayor a 0"

    return True, "OK"

def print_chain(chain):
    """
    Helper para imprimir la cadena en consola de forma legible (Pretty Print).
    """
    print("--- ESTADO ACTUAL DE LA CADENA ---")
    print(json.dumps(chain, indent=4, sort_keys=True))
    print("----------------------------------")