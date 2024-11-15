# transaction을 전파 받았을 때 utxo의 유효성을 검증하고 mempool에 추가

from flask import Flask, Blueprint, request, jsonify
from stack_operator import Stack
from parsing import parse_transaction

bp = Blueprint('utxo_verify', __name__)

@bp.post('/') # POST method로 tx의 body 받아오기

def utxo_verify():
    data = request.get_json() # Json data 받아오기
    print(data)
    print('utxo_verify')
    valid_tx = [] # 검증 과정을 통과한 tx들 저장 후 mempool에 추가
    response_log = [] # response 내용 저장 후 return
    
    try:
        transaction_list = parse_transaction(data)
        print("parsing : " , transaction_list)  
    except Exception as e:
        error_message = f"parsing error: {str(e)}"
        print(error_message) # 오류 메세지
        response_log.append(error_message)
    
    with open("./data/UTXOes.txt", 'r') as utxo_data: # input 의 utxo가 utxo file에 존재하는지 검사
        utxo_list = utxo_data.read().split('\n\n')
        for transaction_data in transaction_list:
            try:
                transaction = transaction_data.split('\n')
                txid = transaction[0] # txid 
                input = transaction[1].split('#') # ptxid#output_index#amount#locking_script#unlocking_script
                outputs = transaction[2:] # output_index#amount#locking_script
                
                for utxo_data in utxo_list:
                    utxo = utxo_data.split('\n')
                    ptxid = utxo[0] # txid
                    utxo_input = utxo[1].split('#') # ptxid#output_index#amount#locking_script#unlocking_script
                    utxo_output = [] # output_index#amount#locing_script
                    for i in range(2, len(utxo)):
                        utxo_output.append(utxo[i].split('#')) # output_index#amount#locking_script
                    i = 0 # 몇 번째 tx인지 count
                    for utxo_output in utxo_output:
                        print("여기임")
                        if (ptxid == input[0] and utxo_output == input[1:4]): # utxo 내에 input_utxo와 일치하는 utxo가 존재하면
                            find = True # utxo 존재
                            locking_script = input[3] # utxo의 locking script와 input의 unlocking script를 연계하여 순차적으로 실행
                            data[i]['locking_script'] = locking_script
                            unlocking_script = input[4]
                            stack = Stack()
                            stack = stack.script_verify(locking_script, unlocking_script, ptxid)
                            result = stack.CHECKFINALRESULT() # 모든 검증 과정을 통과하면 mempool에 tx 추가
                            print("result : ", result)
                            print("find : ", find)
                            if not result:
                                error = "incorrect script" # script error
                                log_message = toString_tx_data(txid, data, False, error)
                                print(log_message)
                                response_log.append(log_message)
                                continue
                            break
                    if find:
                        break
                
                if not find: # uxto가 존재하지 않는다면
                    error = "UTXO not found" # UTXO error
                    log_message = toString_tx_data(txid, data, False, error)
                    print(log_message)
                    response_log.append(log_message)
                    continue
                
                total_output_amount = 0
            
                for output in outputs:
                    total_output_amount += int(output.split('#')[1])
                print("여긴가")
                if not (int(input[2]) == total_output_amount):
                    error = "amount error"
                    log_message = toString_tx_data(txid, data, False, error)
                    print(log_message)
                    response_log.append(log_message)
                    continue
                print("설마여기?")
                print("txid : ", txid)
                print("data : ", data)
                # 이 검증을 모두 통과하면 mempool에 추가
                log_message = toString_tx_data(txid, data, True)
                print(log_message)
                response_log.append(log_message)
                transaction = '\n'.join(transaction)
                valid_tx.append(transaction)
            except Exception as e:
                # 원인 불명의 오류 발생
                error_message = f"Transaction verification error: {str(e)}"
                print(error_message)
                response_log.append(error_message)
                continue
    print("valid_tx : ", valid_tx)
    # 이 tx를 유효한 tx로 판정하고 mempool에 추가 (tx 실행은 추후에 요청이 들어오면 수행.)
    with open('./data/mempool.txt', 'a') as mempool:
        for transaction in valid_tx:
            mempool.write('\n')
            mempool.write(transaction)
            mempool.write('\n')
    
    # 반환할 결과를 JSON 형태로 변환하여 클라이언트에 응답
    return jsonify({"logs": response_log}), 200


    # 출력형식에 맞춰서 유효성 검증의 결과를 출력
def toString_tx_data(txid, data, valid, error = ''):
    result = []
    result.append(f"transaction: {txid}")
    for tx_data in data:
        print(tx_data)
        tx_input = tx_data.get('input')
        print(tx_input)
        result.append(f"  input: ptxid={tx_input.get('ptxid')}, output_index={tx_input.get('output_index')}, locking_script={tx_data.get('locking_script')}, unlocking_script={tx_input.get('unlocking_script')}")
        print(result)
        i = 0
        for tx_output in tx_data.get('outputs'):
            print(tx_output)
            result.append(f"  output_index:{i} amount={tx_output.get('amount')}, locking_script={tx_output.get('locking_script')}")
            i += 1
        if valid:
            result.append("  validity check: passed")
        else:
            result.append("  validity check: failed")
            result.append('                 ' + 'failed at ' + error)
        result.append("")  # Blank line
    print("\n".join(result))
    # 결과를 하나의 문자열로 반환
    return "\n".join(result)
