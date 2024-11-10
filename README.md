# 📦 Blockchain Project

**A Python-based blockchain project that implements transaction verification and UTXO management.**

## 📜 Project Overview

This project is designed to simulate **transaction validation** as performed in a Bitcoin node, 
using a **virtual stack-based execution engine**. 

The node uses this execution engine to run Bitcoin scripts in formats like 
**P2PKH (Pay-to-PubKey-Hash)**, **P2SH (Pay-to-Script-Hash)**, and **Multisignature**, 
producing validation results.

The execution engine maintains a **UTXO set**, a **STXO set**, and a **Mempool**, 
sequentially executing each transaction’s script along with the corresponding UTXO script that it references.

As an educational project aimed at **enhancing understanding of course material**, 
it focuses on implementing core functionality with a simplified approach, 
including assumptions and constraints to reduce complexity.

## ⚙️ Key Features

- **UTXO Verification** (`utxo_verify.py`)  
  - Verifies the validity of received transactions within the UTXO set.

- **Transaction Processing** (`transaction.py`)  
  - Executes verified transactions from the mempool, adding their outputs to the UTXO set, removing spent UTXOs, and recording used transactions in the STXO set.

- **Main Full Node** (`fullnode.py`)  
  - Integrates all route functions, forming the main process of the blockchain network.

- **Blueprint-Based Route Structure**  
  - Uses Flask’s Blueprint for modular route management.

## 📂 Folder Structure

```plaintext
Blockchain_Project/
├── fullnode.py               # Main Flask application file
├── parsing.py                # Parses and processes incoming transaction requests
├── query.py                  # Processes and sends transaction query requests to the main node (fullnode.py)
├── stack_operator.py         # Manages stack operations for script instructions (OP codes)
├── txid_function.py          # Generates transaction IDs (txid)   
├── route/                    # Folder for route management
│   ├── __init__.py           # Blueprint initialization file
│   ├── transaction.py        # Transaction processing route
│   └── utxo_verify.py        # UTXO verification route
└── data/                     # Folder for storing blockchain-related data files
    ├── transaction.txt       # STXO set (Spent Transaction Outputs)
    ├── UTXOex.txt            # UTXO set (Unspent Transaction Outputs)
    └── mempool.txt           # Mempool, temporarily holding pending transactions
```

### Data Files in `data/` Folder

- **`transaction.txt`**  
  - Represents the **STXO set**, containing records of spent transaction outputs.

- **`UTXOex.txt`**  
  - Represents the **UTXO set**, storing records of unspent transaction outputs that are available for new transactions.

- **`mempool.txt`**  
  - Functions as the **Mempool**, holding unconfirmed transactions waiting to be processed.

## 🚀 Installation & Execution

### 1. Git Clone: Clone the project to your local machine.

```bash
git clone https://github.com/seonghwan20/Blockchain_Project.git
cd Blockchain_Project
```

### 2. Install Required Packages

This project requires Flask and ECDSA

- **Flask**: A lightweight web framework for Python, used in this project for handling HTTP requests, managing routes, and creating endpoints for blockchain interactions. Flask’s modularity allows the project to define routes efficiently and manage server-side processes for the blockchain node.
  
- **ecdsa**: A Python library implementing the Elliptic Curve Digital Signature Algorithm, essential for generating and verifying digital signatures within blockchain transactions. This is used to ensure transaction authenticity and integrity by signing transactions and verifying their signatures, which is fundamental to secure transaction processing.

```bash
pip install Flask
pip install ECDSA
```

### 3. Start the Server

Run the main process (`fullnode.py`) to start the Flask server.

```bash
python fullnode.py
```

### 4. Access the Local Server

In a web browser, go to `http://localhost:5000` to test the blockchain full node functionality.

## 📌 Usage Examples

- **UTXO Verification**  
  Access the `/utxo_verify` endpoint to check if a submitted transaction is valid in the UTXO set.

- **Transaction Processing**  
  Send verified transactions to the `/transaction` endpoint to update the UTXO set.

## 🔨 Code Overview

- **`fullnode.py`**
  - Flask Application: Manages the main processes of the full node, integrating all route endpoints.
  - Blueprint Registration: Registers routes defined in `utxo_verify.py` and `transaction.py` as Blueprints for modular route management.

- **`route/utxo_verify.py`**
  - **UTXO Verification**: Validates whether a transaction can spend specific UTXOs within the UTXO set and returns the verification result.

- **`route/transaction.py`**
  - **Transaction Execution**: Executes validated transactions from the mempool, adding their outputs to the UTXO set, removing spent UTXOs, and recording spent transactions in the STXO set (`transaction.txt`).


## 🛠 Tech Stack

- **Python 3**
- **Flask**: Web framework for route management
- **Blueprint**: Used for modular route management
