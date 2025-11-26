# ⛓️ Simple Python Blockchain

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Educational-orange)

Una implementación funcional y educativa de una **Blockchain descentralizada** escrita en Python.  
Este proyecto fue desarrollado para comprender los principios fundamentales de la tecnología blockchain:  
**Inmutabilidad, Proof-of-Work, Hashing Criptográfico y Arquitectura Distribuida.**

---

## 🚀 Características Principales

- **Bloques y Hashing:** SHA-256 enlazando cada bloque.
- **Proof-of-Work:** Algoritmo de minería básico.
- **Transacciones:** Envío de "monedas" entre direcciones.
- **Red P2P (Simulada):** Ejecución de múltiples nodos en distintos puertos.
- **Consenso:** Resolución de conflictos mediante el algoritmo de “Cadena más larga”.
- **API REST:** Implementada con Flask.

---

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/simple-blockchain.git
cd simple-blockchain
```

### 2. Crear entorno virtual (opcional, recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 💻 Uso y Ejecución

Podés ejecutar un nodo o simular una red completa con múltiples nodos.

### 🟦 1. Iniciar el Nodo Principal
```bash
python node.py -p 5000
```

El nodo estará activo en:  
👉 http://localhost:5000

### 🟩 2. Iniciar un Segundo Nodo (Opcional)
```bash
python node.py -p 5001
```

---

## 📡 Interactuando con la API

Podés usar **Postman, cURL o el navegador**.

### 🔨 1. Minar un bloque
```bash
curl -X GET http://localhost:5000/mine
```

### 💸 2. Crear una transacción
```bash
curl -X POST http://localhost:5000/transactions/new \
-H "Content-Type: application/json" \
-d '{"sender": "d4ee26...", "recipient": "address-bob", "amount": 5}'
```

### 🔍 3. Ver la cadena completa
```bash
curl -X GET http://localhost:5000/chain
```

---

## 🌐 Simulación de Red y Consenso

Si tenés dos nodos (5000 y 5001), podés probar el consenso:

### Registrar nodos
```bash
curl -X POST http://localhost:5000/nodes/register \
-H "Content-Type: application/json" \
-d '{"nodes": ["http://127.0.0.1:5001"]}'
```

### Generar conflicto entre nodos
1. Miná **1 bloque** en el nodo 5000.  
2. Miná **3 bloques** en el nodo 5001 (cadena más larga).

### Resolver conflicto
```bash
curl -X GET http://localhost:5000/nodes/resolve
```

**Resultado:**  
El nodo 5000 adoptará la cadena del 5001 por ser más larga y válida.

---

## 📂 Estructura del Proyecto

```
simple-blockchain/
│
├── node.py             # Punto de entrada - inicia el servidor Flask.
├── api.py              # Endpoints de la API REST.
├── blockchain.py       # Lógica de la Blockchain, bloques y consenso.
├── utils.py            # Funciones auxiliares.
├── requirements.txt    # Dependencias.
└── README.md           # Documentación.
```

---

## 🧩 Conceptos Clave

### 🔐 Proof of Work (PoW)
El sistema busca un `nonce` que haga que el hash del bloque empiece con `0000`.  
Esto garantiza:
- Costos computacionales para minar
- Verificación rápida

### 📌 Inmutabilidad
Cada bloque contiene el `previous_hash`.  
Modificar un bloque invalida todos los posteriores, protegiendo la cadena.

---

## 📄 Licencia

Proyecto bajo licencia **MIT**.  
Ver archivo `LICENSE` para más información.

---

**Hecho por Santiago Domínguez**
