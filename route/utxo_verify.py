# transaction을 전파 받았을 때 utxo의 유효성을 검증하고 mempool에 추가

from flask import Flask, Blueprint, Request, jsonify

bp = Blueprint('utxo_verify', __name__)

@bp.route('/utxo_verify', method = ['POST']) # POST method로 tx의 body 받아오기

def utxo_verify():
    data = Request.get_json() # Json data 받아오기
    txid = data.get('txid') # tx id 받아오기
    input = data.get('input') # input 정보 받아오기 [<utxo>, <unlocking script>]
    output = data.get('output') # output 정보 받아오기 [index, <amount>, <locking script>]
    
    with open('../data/UTXOes.txt', 'r') as utxo_data: # input 의 utxo가 utxo file에 존재하는지 검사
        utxo_list = [utxo.split('#') for utxo in utxo_data.read().split('>')] # utxo 형식 : >ptxid#output_index#amount(단위: satoshi)#locking_script
        find = False # utxo의 존재 여부
        for utxo in range(utxo_list):
            if (utxo[0] == input[0][0] | utxo[1] == input[0][1] | utxo[2] >= input[0][2]): # utxo 내에 txid와 output index가 전부 일치하는 tx가 존재하고, 그 금액이 input의 amount보다 크다면
                        # utxo의 locking script(uxto[3])와 input의 unlocking script(input[1])를 연계하여 순차적으로 실행
                        # 기존 utxo를 삭제하고 file의 맨 뒤에 이번 tx의 output들을 추가
                find = True # utxo 존재
        if not find: # uxto가 존재하지 않는다면
            # "utxo 집합에 존재하지 않는 utxo입니다." 예외 처리
            
        total_output_amount = 0
        for output in output:
            total_output_amount += output[1]
        if (input[0][2] = total_output_amount):
            # 바로 통과
        elif (input[0][2] > total_output_amount):
            # 나 자신에게 다시 보내는 output을 생성해 body에 추가
        elif (input[0][2] < total_output_amount): # utxo의 amount 보다 output들의 amount를 합친 것이 더 크다면
            # "올바르지 않은 amount입니다." 예외 처리
        # utxo의 locking script를 input의 unlocking script로 해제할 수 있다면 통과
        # 그렇지 못한다면 "올바르지 않은 script입니다" 예외 처리
        
        # 이 세가지 검증을 모두 통과하면 
        # 이 tx를 유효한 tx로 판정하고 mempool에 추가 (tx 실행은 추후에 요청이 들어오면 수행.)
        
        # 출력형식에 맞춰서 유효성 검증의 결과를 출력