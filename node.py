from argparse import ArgumentParser
from api import app

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-p', '--port', default=5000, type=int, help='Puerto para escuchar')
    parser.add_argument('-H', '--host', default='0.0.0.0', type=str, help='Host IP')

    args = parser.parse_args()
    port = args.port
    host = args.host

    print("=========================================")
    print("🚀 Iniciando Nodo Blockchain")
    print(f"📡 Escuchando en: http://{host}:{port}")
    print("⛓️  ID del Nodo: (Gestionado en api.py)")
    print("=========================================")

    app.run(host=host, port=port)
