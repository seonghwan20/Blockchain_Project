# transaction을 전파 받았을 때 utxo의 유효성을 검증하고 mempool에 추가

from flask import Flask, Blueprint, request, jsonify
from stack_operator import Stack
from parsing import parse_transaction

bp = Blueprint('utxo_verify', __name__)

@bp.route('/utxo_verify', methods = ['POST']) # POST method로 tx의 body 받아오기

def utxo_verify():
    data = request.get_json() # Json data 받아오기
    valid_tx = [] # 검증 과정을 통과한 tx들 저장 후 mempool에 추가
    response_log = [] # response 내용 저장 후 return
    
    try:
        transaction_list = parse_transaction(data)
    except Exception as e:
        error_message = f"parsing error: {str(e)}"
        print(error_message) # 오류 메세지
        response_log.append(error_message)
    
    with open('../data/UTXOes.txt', 'r') as utxo_data: # input 의 utxo가 utxo file에 존재하는지 검사
        utxo_list = utxo_data.read().split('\n\n') # utxo 형식 : ptxid#output_index#amount(단위: satoshi)#locking_script
        utxo_data_list = []
        
        for utxo in utxo_list: # utxo data를 파싱해서 리스트로 저장
            utxo_data = utxo_data.split('#')
            utxo_data_list.append(utxo_data)
            
        for transaction_data in transaction_list:
            try:
                txid = transaction_data[0]
                transaction = transaction_data[1]
                find = False # utxo의 존재 여부
                input = transaction.get("input")[0] # input dictionary data 받아오기
                outputs = transaction.get("outputs") # output dictionary data 받아오기
                unlocking_script = input.get("unlocking_script").split(' ') # unlocking script 파싱해서 저장
                input_utxo = input.get("utxo") # utxo data 받아오기
                _, input_utxo = input_utxo.split('>')
                input_utxo = input_utxo.split('#')
                
                for utxo in utxo_data_list: # [0] : ptxid, [1] : output index, [2] : amount, [3] : locking script
                    if (utxo[0] == input_utxo[0] and utxo[1] == input_utxo[1] and utxo[2] >= input_utxo[2]): # utxo 내에 txid와 output index가 전부 일치하는 tx가 존재하고, 그 금액이 input의 amount보다 크다면
                        find = True # utxo 존재
                        locking_script = utxo[3].split(' ') # utxo의 locking script(uxto[3])와 input의 unlocking script(input[1])를 연계하여 순차적으로 실행
                        stack = Stack()
                        stack = stack.script_verify(locking_script, unlocking_script)
                        result = stack.CHECKFINALRESULT() # 모든 검증 과정을 통과하면 mempool에 tx 추가
                        if not result:
                            error = "incorrect script" # script error
                            log_message = toString_tx_data(txid, transaction, False, error)
                            print(log_message)
                            response_log.append(log_message)
                            continue
                        
                if not find: # uxto가 존재하지 않는다면
                    error = "UTXO not found" # UTXO error
                    log_message = toString_tx_data(txid, transaction, False, error)
                    print(log_message)
                    response_log.append(log_message)
                    continue
                
                total_output_amount = 0
            
                for output in outputs:
                    total_output_amount += int(output.get("amount"))
                
                if not (int(input_utxo[2]) == total_output_amount):
                    error = "amount error"
                    log_message = toString_tx_data(txid, transaction, False, error)
                    print(log_message)
                    response_log.append(log_message)
                    continue
                    
                # 이 검증을 모두 통과하면 mempool에 추가
                log_message = toString_tx_data(txid, transaction, True)
                print(log_message)
                response_log.append(log_message)
                valid_tx.append((txid, transaction))
            except Exception as e:
                # 원인 불명의 오류 발생
                error_message = f"Transaction verification error: {str(e)}"
                print(error_message)
                response_log.append(error_message)
                continue
    
    # 이 tx를 유효한 tx로 판정하고 mempool에 추가 (tx 실행은 추후에 요청이 들어오면 수행.)
    with open('../data/mempool.txt', 'a') as mempool:
        for txid, transaction in valid_tx:
            # txid 저장
            mempool.write(f"{txid}\n")
            
            # input 저장 (각 필드를 '#'로 구분)
            tx_input = transaction["inputs"][0]
            mempool.write(f"{tx_input['utxo']}#{tx_input['unlocking_script']}\n")
            
            # output 저장 (각 필드를 '#'로 구분, 여러 개의 output을 순차적으로 저장)
            for tx_output in transaction["outputs"]:
                mempool.write(f"{tx_output['output_index']}#{tx_output['amount']}#{tx_output['locking_script']}\n")
            
            # transaction 간 Blank line 추가
            mempool.write("\n")
    
    # 반환할 결과를 JSON 형태로 변환하여 클라이언트에 응답
    return jsonify({"logs": response_log}), 200


    # 출력형식에 맞춰서 유효성 검증의 결과를 출력
def toString_tx_data(txid, tx_data, valid, error = ''):
    result = []
    result.append(f"transaction: {txid}")
    for tx_input in tx_data['inputs']:
        result.append(f"  input: utxo={tx_input['utxo']}, unlocking_script={tx_input['unlocking_script']}")
    for tx_output in tx_data['outputs']:
        result.append(f"  output:{tx_output['output_index']} amount={tx_output['amount']}, locking_script={tx_output['locking_script']}")
    if valid:
        result.append("  validity check: passed")
    else:
        result.append("  validity check: failed")
        result.append('                 ' + 'failed at ' + error)
    result.append("")  # Blank line

    # 결과를 하나의 문자열로 반환
    return "\n".join(result)
