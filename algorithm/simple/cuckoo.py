

import hashlib,random
from typing import Optional,List

def position_hash(i:int,data:bytes,n:int) -> int:
    length = (n.bit_length() +7) // 8

    h = hashlib.sha256(bytes([i]) + data).digest()[:length]
    val = int.from_bytes(h,"big")

    return val % n


class CuckooHashTable:
    def __init__(self,n:int,s:int, max_depth=500):
        self._n = n
        self._s = s
        self._table:List[Optional[bytes]] = self._n * [None]
        self._table_hash_index = self._n * [(-1,-1)]
        self._stash:List[Optional[bytes]] = self._s * [None]
        self._stash_count = 0
        self._max_depth = max_depth
        self._conflict_times = 0


    def update(self,data:bytes):
        for _ in range(self._max_depth):
            #hash1
            h1 = position_hash(1,data,self._n)
            if self._table[h1] is None:
                self._table[h1] = data
                self._table_hash_index[h1] = (h1,1)
                return

            #hash2
            h2 = position_hash(2, data, self._n)
            if self._table[h2] is None:
                self._table[h2] = data
                self._table_hash_index[h2] = (h2,1)
                return

            h3 = position_hash(3, data, self._n)
            if self._table[h3] is None:
                self._table[h3] = data
                self._table_hash_index[h3] = (h3,1)
                return

            i = random.randrange(3)
            h = [h1,h2,h3][i]
            old_data = self._table[h]
            self._table[h] = data
            self._table_hash_index[h] = (h,i+1)

            data = old_data
            self._conflict_times+=1

        if self._stash_count >= self._s:
            raise ValueError("too few capacity for stash")


        self._stash[self._stash_count] = data
        self._stash_count+=1

    @property
    def table(self) -> List[Optional[bytes]]:
        return self._table

    @property
    def stash(self) -> List[Optional[bytes]]:
        return self._stash

    @property
    def table_hash_index(self):
        return self._table_hash_index

    @property
    def conflict_times(self) -> int:
        return self.conflict_times

    @property
    def stash_numbers(self) -> int:
        return self._stash_count