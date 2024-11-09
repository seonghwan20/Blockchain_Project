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

## ⚙️ Features

- **UTXO Verification** (`utxo_verify.py`)  
  - Verifies if received transactions are spendable within the UTXO set.

- **Transaction Processing** (`transaction.py`)  
  - Processes verified transactions to update the UTXO set.

- **Main Full Node** (`fullnode.py`)  
  - Integrates all route functions, forming the main process of the blockchain network.

- **Blueprint-Based Route Structure**  
  - Uses Flask’s Blueprint for modular route management.

## 📂 Folder Structure

```plaintext
Blockchain_Project/
├── fullnode.py               # Main Flask application file
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

This project requires Flask and Python 3.

```bash
pip install Flask
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
  - Flask Application: Integrates all routes, forming the main process of the full node.
  - Blueprint Registration: Registers routes defined in `utxo_verify.py` and `transaction.py` as Blueprints.

- **`route/utxo_verify.py`**
  - **UTXO Verification**: Checks if a transaction is spendable within the UTXO set and returns the validity result.

- **`route/transaction.py`**
  - **Transaction Processing**: Processes verified transactions to update the UTXO set.

## 🛠 Tech Stack

- **Python 3**
- **Flask**: Web framework for route management
- **Blueprint**: Used for modular route management
