# transaction을 받을 때  data를 parsing하여 저장되는 구조에 맞게 변경하여 전달

import hashlib
from txid_function import hash_to_txid

def parse_transaction(data):
    # parse transaction list
    transactions = data.get("transactions")

    parsed_transactions = []

    for tx in transactions:
        input = []
        outputs = []
        
        # parse input data
        tx_input = tx.get("input")
        input.append({
                "utxo": tx_input.get("utxo").strip(), # utxo는 >ptxid#output index#amount#locking script 구조
                "unlocking_script": tx_input.get("unlocking_script").strip()
            })

        # parse output data
        for tx_output in tx.get("outputs"):
            outputs.append({
                "output_index": tx_output.get("output_index"),  
                "amount": tx_output.get("amount"),
                "locking_script": tx_output.get("locking_script").strip()
            })

        # transaction data parsing 결과
        transaction_data = {
            "inputs": input,
            "outputs": outputs
        }
        
        txid = create_txid(transaction_data)
        parsed_transactions.append((txid, transaction_data))
    
    def create_txid(transaction):
        txid_data = []

        # input data 추가
        tx_input = transaction["inputs"][0]
        txid_data.append(f"{tx_input['utxo']}#{tx_input['unlocking_script']}")

        # output data 추가
        for tx_output in transaction["outputs"]:
            txid_data.append(f"{tx_output['output_index']}#{tx_output['amount']}#{tx_output['locking_script']}")

        # 모든 요소를 합쳐서 문자열 생성
        tx_string = "\n".join(txid_data)
        
        return hash_to_txid(tx_string)

    return parsed_transactions