# stack 구조 구현
# stack operator 구현
# # OP의 종류 : DUP, HASH, EQUAL, EQUALVERIFY, CHECKSIG, CHECKSIGVERIFY, CHECKMULTISIG, CHECKMULTISIGVERIFY, IF..ELSE..ENDIF, IF..ENDIF, CHECKFINALRESULT

import hashlib
import ecdsa
from itertools import combinations

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def PUSH(self, data):
        if self.top is None:
            self.top = Node(data)
        else:
            node = Node(data)
            node.next = self.top
            self.top = node

    def POP(self):
        if self.top is None:
            return None
        node = self.top
        self.top = self.top.next
        return node.data

    def PEEK(self):
        if self.top is None:
            return None
        return self.top.data

    def IS_EMPTY(self):
        return self.top is None
    
    def DUP(self): 
        if self.top is None:
            return None
        data = self.top.data # data만 뽑아서
        self.PUSH(data) # 다시 PUSH
    
    def HASH(self):
        if self.top is None:
            return None
        node = self.POP
        data_hash = hashlib.sha256(node.data) # data에 hash함수 적용
        data_hash.hexdigest() # 16진수로 변환
        self.PUSH(data_hash) # stack에 PUSH
        
    def EQUAL(self):
        if self.top is None:
            return None
        data_1 = self.POP()
        data_2 = self.POP()
        if (data_1 == data_2): # 두 data 값 비교 후 True or False PUSH
            self.PUSH(True)
        else:
            self.PUSH(False)
    
    def EQUALVERIFY(self):
        if self.top is None:
            return None
        data_1 = self.POP()
        data_2 = self.POP()
        if not (data_1 == data_2): # 두 data 값 비교 후 다르면 return None
            return None
    
    def CHECKSIG(self, txid): # 해당 tx의 input의 utxo의 ptxid를 입력받는다.
        if (self.top is None | self.top.next is None):
            return None
        pubKey = self.POP() # Public Key
        sig = self.POP() # Signature
        tx_hash = find_tx_hash(txid) # tx값에 hash함수 적용해서 return 하는 find_tx_hash 함수 적용
        try:
            pubKey.verify(sig, tx_hash) # 검증이 완료됐다면 stack에 True를 PUSH
            self.PUSH(True)
        except Exception as e:
            self.PUSH(False) # 검증이 실패했다면 stack에 False를 PUSH
            print("서명 검증 실패", str(e)) 
            
    def CHECKSIGVERIFY(self, txid):
        if (self.top is None | self.top.next is None):
            return None
        pubKey = self.POP() # Public Key
        sig = self.POP() # Signature
        tx_hash = find_tx_hash(txid) # tx값에 hash함수 적용해서 return 하는 find_tx_hash 함수 적용
        try:
            pubKey.verify(sig, tx_hash) # 검증이 완료됐다면 오류없이 코드 종료
        except Exception as e:
            print("서명 검증 실패", str(e)) # 검증이 실패했다면 오류 발생
        
    def CHECKMULTISIG(self, txid):
        N = self.POP()
        pubKey_list = []
        for i in range(N):
            pubKey_list.append(self.POP()) # N개의 Public Key 저장
        M = self.POP()
        sig_list = []
        for i in range(M):
            sig_list.append(self.POP()) # M개의 Signature 저장
        
        combinations_list = list(combinations(pubKey_list, M))
        tx_hash = find_tx_hash(txid)

        for comb in combinations_list:
            count = 0 # M개의 sig-pubKey 쌍이 일치하는지 count
            match = False
            for sig in sig_list:
                for pubKey in comb:
                    try:
                        pubKey.verify(sig, tx_hash) 
                        count += 1 # 검증이 성공했다면 count += 1
                    except Exception as e:
                        continue
            if (count == M): # M개의 검증이 성공하면 match = True
                self.POP(True) # stack에 True를 PUSH
                match = True
        if (match == False): # 모든 경우의 수를 확인했지만 검증이 실패했다면 stack에 False를 PUSH
            self.POP(False)
        
    def CHECKMULTISIGVERIFY(self, txid):
        N = self.POP()
        pubKey_list = []
        for i in range(N):
            pubKey_list.append(self.POP()) # N개의 Public Key 저장
        M = self.POP()
        sig_list = []
        for i in range(M):
            sig_list.append(self.POP()) # M개의 Signature 저장
        
        combinations_list = list(combinations(pubKey_list, M))
        tx_hash = find_tx_hash(txid)

        for comb in combinations_list:
            count = 0 # M개의 sig-pubKey 쌍이 일치하는지 count
            match = False
            for sig in sig_list:
                for pubKey in comb:
                    try:
                        pubKey.verify(sig, tx_hash) 
                        count += 1 # 검증이 성공했다면 count += 1
                    except Exception as e:
                        continue
            if (count == M): # M개의 검증이 성공하면 match = True
                match = True
        if (match == False): # 모든 경우의 수를 확인했지만 검증이 실패했다면 return None
            return None
            
    def CHECKFINALRESULT(self):
        if (self.top is not None and self.top.next is None and self.top.data is True):
            return True
        else:
            return False

def find_tx_hash(txid):
    with open('/data/mempool.txt', 'r') as mempool: # mempool에서 utxo를 포함하는 tx의 내용 찾기
        tx_data = mempool.read().split('\n\n') # Blank line으로 구분해서 저장한 후
        tx = [tx for tx in tx_data if txid == tx_data[0]] # txid가 일치하는 tx 내용을 저장 
        tx_hash = hashlib.sha256(tx[0])
        return tx_hash
        