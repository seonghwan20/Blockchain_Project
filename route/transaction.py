# mempool에 쌓여있는 유효한 tx들을 실행시키고 그 tx들의 output을 memepool에 추가

from flask import Blueprint

bp = Blueprint('transaction', __name__)

@bp.route('/transaction',  method = ['GET']) # GET method로 tx처리요청 받기

def transaction():
    with open('../data/mempool.txt', 'r') as tx_data: # mempool에 존재하는 tx list 받아오기
        tx_list = [tx.split('>') for tx in tx_data.read().split('\n')] # 공백으로 tx를 구분하여 이차원 배열로 저장
        stxo_list = [] # 사용한 tx 정보는 따로 저장한 후에 utxo에서 제거
        utxo_list = [] # 새로운 utxo 정보는 따로 저장한 후에 utxo에 추가
        for i in range(len(tx_list)):
            for j in range(len(tx_list[i])):
                tx_list[i][j] = tx_list[i][j].split('#') # 각 tx 마다 데이터 별로 분리하여 삼차원 배열로 저장
                utxo = '>' #
                if (j == 0):
                    utxo += tx_list[[i][j]] # 이 tx의 id 저장
                elif (j == 1):
                    stxo_list.append(tx_list[i][j][0]) # 각 tx의 input data의 utxo id 를 stxo_list에 저장
                elif (j >= 2):
                    utxo += '#' + tx_list[i][j][0] # output index
                    utxo += '#' + tx_list[i][j][1] # amount
                    utxo += '#' + tx_list[i][j][2] # locking script
                    utxo_list.append(utxo)
    
    with open('../data/UTXOes.txt', 'r') as utxo_data: 
        lines = utxo_data.readlines()
        
    for i in range(len(stxo_list)): 
        lines = [line for line in lines if stxo_list[i] not in line] # utxo에서 방금 사용한 tx들의 정보를 제거
    for i in range(len(utxo_list)):
        lines += '\n' + utxo_list[i] + '\n' # utxo 맨 뒤에 방금 생성된 utxo list 추가하기
        
    with open('../data/UTXOes.txt', 'w') as utxo_data:
        utxo_data.writelines(lines) # 수정된 utxo_data로 덮어쓰기
        
    # 출력형식에 맞춰서 tx 처리 결과를 출력 (출력형식은 자유)
        