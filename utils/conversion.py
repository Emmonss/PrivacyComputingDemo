import numpy as np




def bit_arr_to_bytes(arr:np.ndarray) -> bytes:
    n = arr.size
    pad_width = (8-n%8)%8
    arr = np.pad(arr,pad_width=((pad_width,0),), constant_values=0)
    bs = bytes(np.packbits(arr).tolist())
    return int_to_bytes_fix_len(n) + bs


def bytes_to_bit_arr(data:bytes) -> np.ndarray:
    prefix_length = 4
    n = bytes_to_int(data[:prefix_length])

    arr = np.array(list(data[prefix_length:]),dtype=np.uint8)
    res = np.unpackbits(arr)[-n:]
    return res

def int_to_bytes(integer:int):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big')

def bytes_to_int(bytes_arr:bytes):
    return int.from_bytes(bytes_arr, byteorder='big', signed=False)

def int_to_bytes_fix_len(integer:int):
    bytes_length = (integer.bit_length()+7)//8
    bytes_length = (bytes_length+3)//4*4
    bytes_length = 4 if bytes_length == 0 else bytes_length
    if bytes_length >4:
        raise ValueError("too big integer")
    return integer.to_bytes(bytes_length,'big')