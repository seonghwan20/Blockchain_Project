# transaction을 받을 때  data를 parsing하여 저장되는 구조에 맞게 변경하여 전달

import hashlib
from txid_function import hash_to_txid

def parse_transaction(data):
    # parse transaction list
    transactions = data

    parsed_transactions = []
    print('parsing')
    print(transactions)
    for tx in transactions:
        outputs = []
        # parse input data
        tx_input = tx.get("input")
        input ={
            "utxo": tx_input.get("utxo"), # utxo는 >ptxid#output index#amount#locking script 구조
            "unlocking_script": tx_input.get("unlocking_script").strip()
        }
        print('input : ', input)

        # parse output data
        for tx_output in tx.get("outputs"):
            outputs.append({
                "output_index": tx_output.get("output_index"),  
                "amount": tx_output.get("amount"),
                "locking_script": tx_output.get("locking_script").strip()
            })

        # transaction data parsing 결과
        transaction_data = {
            "input": input,
            "outputs": outputs
        }
        
        print(transaction_data)
        
        txid = create_txid(transaction_data)
        print(txid)
        parsed_transactions.append((txid, transaction_data))
        print(parsed_transactions)
    
    return parsed_transactions

def create_txid(transaction):
    txid_data = []

    # input data 추가
    tx_input = transaction.get("input")
    utxo_data = tx_input.get("utxo")
    utxo = f"{utxo_data.get("ptxid")}#{utxo_data.get("output_index")}#{utxo_data.get("amount")}"
    txid_data.append(f"{utxo}#{tx_input.get("unlocking_script")}")

    # output data 추가
    for tx_output in transaction.get("outputs"):
        txid_data.append(f"{tx_output.get("output_index")}#{tx_output.get("amount")}#{tx_output.get("locking_script")}")

    # 모든 요소를 합쳐서 문자열 생성
    tx_string = "\n".join(txid_data)
    print(txid_data)
    print(tx_string)
    return hash_to_txid(tx_string)

    