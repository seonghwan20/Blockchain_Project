#txid를 생성하는 function

import hashlib

def hash_to_txid(transaction_string):
    lines = transaction_string.strip().split('\n')

    # 첫 번째 줄(txid)을 제외한 나머지 줄들을 합침
    data_to_hash = "\n".join(lines)  # txid를 제외한 나머지 transaction 정보들

    # data를 UTF-8로 encoding하고 SHA-256 HASH 생성
    txid = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
    return txid