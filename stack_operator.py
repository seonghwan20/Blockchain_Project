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
        print("여긴가?")
        node = self.POP()
        data_hash = hashlib.sha256(node.encode('utf-8')).hexdigest() # data에 hash함수 적용
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
        if (self.top is None or self.top.next is None):
            return None
        pubKey = self.POP() # Public Key
        sig = self.POP() # Signature
        try:
            if sig_verify(sig, pubKey, txid): # 검증이 완료됐다면 stack에 True를 PUSH
                self.PUSH(True)
            else:
                self.PUSH(False) # 검증이 실패했다면 stack에 False를 PUSH    
        except Exception as e:
            self.PUSH(False) # 검증에 오류가 발생했다면 stack에 False를 PUSH
            print("CHECKSIG Error", str(e)) 
            
    def CHECKSIGVERIFY(self, txid):
        if (self.top is None or self.top.next is None):
            return None
        pubKey = self.POP() # Public Key
        sig = self.POP() # Signature
        try:
            if sig_verify(sig, pubKey, txid): # 검증이 완료됐다면 stack에 True를 PUSH
                self.PUSH(True)
            else:
                self.PUSH(False) # 검증이 실패했다면 stack에 False를 PUSH    
        except Exception as e:
            self.PUSH(False) # 검증에 오류가 발생했다면 stack에 False를 PUSH
            print("CHECKSIGVERIFY Error", str(e)) 
        
    def CHECKMULTISIG(self, txid):
        N = self.POP()
        pubKey_list = [self.POP() for _ in range(N)]  # N개의 Public Key를 stack에서 꺼내서 저장
        M = self.POP()
        sig_list = [self.POP() for _ in range(M)]  # M개의 Signature를 stack에서 꺼내서 저장
        
        combinations_list = list(combinations(pubKey_list, M))
        
        for comb in combinations_list:
            count = 0 # M개의 sig-pubKey 쌍이 일치하는지 count
            match = False
            for sig in sig_list:
                for pubKey in comb:
                    try:
                        if sig_verify(sig, pubKey, txid) :
                            count += 1 # 검증이 성공했다면 count += 1
                            break  # 검증이 성공하면 해당 Public Key 조합 내 다른 Public Key는 건너뜀
                        else:
                            continue
                    except Exception as e:
                        print("CHECKMULTISIG Error", str(e))
                        continue
            if (count == M): # M개의 검증이 성공하면 match = True
                self.PUSH(True) # stack에 True를 PUSH
                match = True
                break
            
        if (match == False): # 모든 경우의 수를 확인했지만 검증이 실패했다면 stack에 False를 PUSH
            self.PUSH(False)
        
    def CHECKMULTISIGVERIFY(self, txid):
        N = self.POP()
        pubKey_list = [self.POP() for _ in range(N)]  # N개의 Public Key를 stack에서 꺼내서 저장
        M = self.POP()
        sig_list = [self.POP() for _ in range(M)]  # M개의 Signature를 stack에서 꺼내서 저장
        
        combinations_list = list(combinations(pubKey_list, M))

        for comb in combinations_list:
            count = 0 # M개의 sig-pubKey 쌍이 일치하는지 count
            match = False
            for sig in sig_list:
                for pubKey in comb:
                    try:
                        if sig_verify(sig, pubKey, txid) :
                            count += 1 # 검증이 성공했다면 count += 1
                            break  # 검증이 성공하면 해당 Public Key 조합 내 다른 Public Key는 건너뜀
                        else:
                            continue
                    except Exception as e:
                        print("CHECKMULTISIG Error", str(e))
                        continue
            if (count == M): # M개의 검증이 성공하면 match = True
                match = True
                break
        if not match: # 모든 경우의 수를 확인했지만 검증이 실패했다면 return None
            print("CHECKMULTISIGVERIFY failed")  # 오류 발생
            
    def CHECKFINALRESULT(self):
        if (self.top is not None and self.top.next is None and self.top.data is True):
            return True
        else:
            return False
        
    def script_verify(self, locking_script, unlocking_script, txid):
        # P2SH = False
        # if locking_script[-1] == 'EQUALVERIFY': # P2SH 방식일 때
        #     redeem_script = unlocking_script[-1].split(' ') # redeem script 저장
        #     P2SH = True

        # OP 코드를 딕셔너리에 매핑
        OP = {
            "DUP": Stack.DUP,
            "HASH": Stack.HASH,
            "EQUAL": Stack.EQUAL,
            "EQUALVERIFY": Stack.EQUALVERIFY,
            "CHECKSIG": Stack.CHECKSIG,
            "CHECKSIGVERIFY": Stack.CHECKSIGVERIFY,
            "CHECKMULTISIG": Stack.CHECKMULTISIG,
            "CHECKMULTISIGVERIFY": Stack.CHECKMULTISIGVERIFY,
            "CHECKFINALRESULT": Stack.CHECKFINALRESULT
        }

        # unlocking script를 stack에 PUSH
        unlocking_script_data = unlocking_script.split(' ')
        for data in unlocking_script_data:
           self.PUSH(data)
        
        locking_script_data = locking_script.split(' ')
        # locking script를 stack에 PUSH
        for data in locking_script_data:
            if data in OP:
                if data in ["CHECKSIG", "CHECKSIGVERIFY", "CHECKMULTISIG", "CHECKMULTISIGVERIFY"]:
                    OP[data](self, txid)
                else:
                    OP[data](self) # OP Dictionary에서 해당 연산을 stack 객체에 적용
            else:
                self.PUSH(data) # data일 경우, stack에 PUSH
                
        # if P2SH: # P2SH 형식이며, locking script의 EQUALVERIFY도 무사히 통과했을 경우
        #     i = 0
        #     while i < len(redeem_script):
        #         data = redeem_script[i] 
        #         if data == 'IF': # data가 IF일 경우
        #             if self.POP().data == True: # top.data가 True일 경우
        #                 i += 1 # IF 뒤의 script를 실행한다
        #                 continue
        #             else: # top.data가 False일 경우
        #                 while data not in ['ELSE', 'ENDIF']: # ELSE or ENDIF가 나올 때 까지 진행
        #                     i += 1
        #                     data = redeem_script[i]
        #                 i += 1 # 그 다음 script부터 실행한다.
        #                 continue
        #         elif data == 'ENDIF': # data가 ENDIF일 경우
        #             i += 1
        #             if i == len(redeem_script): # redeem script가 끝났으면 결과 값 리턴
        #                 return self
        #             else: # 코드가 더 있을 경우 계속 진행
        #                 continue
        #         elif data in OP: # data가 operator일 때
        #             OP[data](self)
        #         else: # data가 일반 data일 때
        #             self.PUSH(data)
        #         i += 1
        
        
        
        return self
    
def sig_verify(sig, pubKey, txid):
    sig_bytes = bytes.fromhex(sig) # hex로 받은 데이터를 bytes 형식으로 변환
    pubKey_bytes = bytes.fromhex(pubKey)
    txid_bytes = bytes.fromhex(txid)

    public_key = ecdsa.VerifyingKey.from_string(pubKey_bytes, curve = ecdsa.SECP256k1)

    is_valid = public_key.verify(sig_bytes, txid_bytes) # 검증 결과 리턴
    
    return is_valid