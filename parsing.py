# transaction을 받을 때  data를 parsing하여 저장되는 구조에 맞게 변경하여 전달

import hashlib

def parse_transaction(data):
    # parse transaction list
    transactions = data

    parsed_transactions = []
    print('parsing')
    print(transactions)
    for tx in transactions:
        # generate txid
        # parse input data
        tx_input = tx.get("input")
        utxo = tx_input.get("utxo") # utxo는 ptxid#output index#amount#locking script 구조
        ptxid = utxo.get("ptxid")
        utxo_output_index = utxo.get("output_index")
        amount = utxo.get("amount")
        locking_script = utxo.get("locking_script")
        unlockingscript = tx_input.get("unlocking_script").strip()
        input = ptxid + '#' + utxo_output_index + '#' + amount + '#' + locking_script + '#' + unlockingscript
        print('input : ', input)

        # parse output data
        output = []
        for tx_output in tx.get("outputs"):
            output_index = tx_output.get("output_index"),  
            amount = tx_output.get("amount"),
            locking_script = tx_output.get("locking_script").strip()
            output_data =  output_index + '#' + amount + '#' + locking_script + '\n'
            output.append(output_data)
        output = '\n'.join(output)
        
        # transaction data parsing 결과
        transaction_data = hashlib.sha256(transaction_data).hexdigest() + '\n' + input + '\n' + output
        print(transaction_data)
        parsed_transactions.append(transaction_data)
    
    return parsed_transactions