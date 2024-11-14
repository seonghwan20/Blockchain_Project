# transaction을 받을 때  data를 parsing하여 저장되는 구조에 맞게 변경하여 전달

import hashlib

def parse_transaction(data):
    # parse transaction list
    parsed_transactions = []
    with open("./data/UTXOes.txt") as utxo_data_set:
        utxo_data = utxo_data_set.read().split('\n\n')
        for tx in data:
            tx_input = tx.get("input")
            tx_outputs = tx.get("outputs")
            print("여기까지")
            ptxid = tx_input.get("ptxid")
            input_output_index = tx_input.get("output_index")
            for utxo in utxo_data:
                utxo = utxo.split('\n')
                utxo_txid = utxo[0]
                utxo_find = False # utxo 일치 여부 확인
                if utxo_txid == ptxid:
                    for utxo_output_data in utxo[2:]:
                        index, utxo_amount, locking_script = utxo_output_data.split('#')
                        if int(input_output_index) == int(index):
                            utxo_find = True
                            break
                if utxo_find:
                    break
            if not utxo_find:
                raise ValueError("UTXO not found")  
                 
            unlocking_script = tx_input.get("unlocking_script")
            
            input = ptxid + '#' + str(index) + '#' + str(utxo_amount) + '#' + locking_script + '#' + unlocking_script
            input_without_unlockingscript =  ptxid + '#' + str(index) + '#' + str(utxo_amount) + '#' + locking_script
            
            # parse output data
            outputs = []
            idx = 0
            for tx_output in tx_outputs:
                output_index = idx
                amount = tx_output.get("amount")
                locking_script = tx_output.get("locking_script").strip()
                output_data =  str(output_index) + '#' + str(amount) + '#' + locking_script
                outputs.append(output_data)
                idx += 1
            output = '\n'.join(outputs)
            
            # transaction data parsing 결과
            transaction_data_without_unlockingscript = input_without_unlockingscript + '\n' + output
            transaction_data = hashlib.sha256(transaction_data_without_unlockingscript.encode('utf-8')).hexdigest() + '\n' + input + '\n' + output
            parsed_transactions.append(transaction_data)
    
    return parsed_transactions