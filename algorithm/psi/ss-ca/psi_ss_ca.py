
import random
import numpy as np
from gmpy2 import mpz
from algorithm.base.hash import compute_sha256
from algorithm.ss.ss_simple import ss_mul


def pad_array_to_length(array, target_length=8):
    # 计算需要补零的数量
    padding_length = target_length - len(array)

    # 如果数组长度小于目标长度，则补零
    if padding_length > 0:
        padded_array = array + [0] * padding_length
    else:
        padded_array = array[:target_length]  # 如果超过目标长度，截断数组

    return padded_array
def split_xor(value):
    # 确保生成的 num1 和 num2 不为零
    num1 = random.randint(1, value - 1)
    num2 = value ^ num1
    return num1, num2

def split_xor_list(value_list):
    length = len(value_list)
    num1_list = [random.randint(0, 1) for _ in range(length)]
    num2_list = [value_list[i] ^ num1_list[i] for i in range(length)]
    return num1_list,num2_list

def list_xor(list1,list2,pad_len=4):
    list1 = pad_array_to_length(list1,pad_len)
    list2 = pad_array_to_length(list2, pad_len)
    return [list1[i]^list2[i] for i in range(pad_len)]

def int_to_binary_array(n,pad_len=4):
    binary_string = bin(n)[2:]
    # 将二进制字符串转换为数组
    binary_array = [int(bit) for bit in binary_string]
    return pad_array_to_length(binary_array,target_length=pad_len)


def bin_arr_to_num(binary_array):
    # 将数组转换为字符串
    binary_string = ''.join(str(bit) for bit in binary_array)
    # 将二进制字符串转换为整数
    return int(binary_string, 2)

def generate_boolean_triplet():
    (a0, b0, c0), (a1, b1, c1) = (0,0,0),(0,0,0)
    while((a0, b0, c0)==(a1, b1, c1)):
        # 随机生成 a0, a1, b0, b1
        a0 = random.randint(0, 1)
        a1 = random.randint(0, 1)
        b0 = random.randint(0, 1)
        b1 = random.randint(0, 1)
        result = (a0 ^ a1) and (b0 ^ b1)
        c0 = random.randint(0, 1)
        c1 = c0 ^ result
    return (a0,b0,c0),(a1,b1,c1)

def bool_bit_and(init_z0,init_z1, next_x0,next_x1,triplet=None):
    if triplet is None:
        triplet = generate_boolean_triplet()
    (a0, b0, c0), (a1, b1, c1) = triplet
    # print(f"a0,b0,c0:{(a0, b0, c0)}")
    # print(f"a1,b1,c1:{(a1, b1, c1)}")
    # print(f"(a0^a1) and (b0^b1):{(a0^a1) and (b0^b1)},c0^c1:{c0^c1}")

    e0 = a0 ^ init_z0
    f0 = b0 ^ next_x0
    e1 = a1 ^ init_z1
    f1 = b1 ^ next_x1
    e = e0 ^ e1
    f = f0 ^ f1
    # print(f"e0:{e0},f0:{f0}")
    # print(f"e1:{e1},f1:{f1}")
    # print(f"e:{e},f1:{f}")

    z0 = (0 and e and f) ^ (f and a0) ^ (e and b0) ^ c0
    z1 = (1 and e and f) ^ (f and a1) ^ (e and b1) ^ c1

    return z0,z1

def compare_two_item(item1,item2,pad_len=64):
    x1_hash = compute_sha256(item1)[:16]
    x2_hash = compute_sha256(item2)[:16]

    decimal_value1 = int(x1_hash, 16)
    decimal_value2 = int(x2_hash, 16)

    decimal_value1_bin = int_to_binary_array(decimal_value1,pad_len)
    decimal_value2_bin = int_to_binary_array(decimal_value2,pad_len)

    x10, x11 = split_xor_list(decimal_value1_bin)
    x20, x21 = split_xor_list(decimal_value2_bin)

    tmp0_xor = list_xor(x10, x20, pad_len)
    tmp0_bin = [1 ^ v for v in tmp0_xor]

    tmp1_bin = list_xor(x11,x21,pad_len)

    z0 = tmp0_bin[0]
    z1 = tmp1_bin[0]

    for i in range(1, pad_len):
        next_x0 = tmp0_bin[i]
        next_x1 = tmp1_bin[i]
        z0, z1 = bool_bit_and(z0, z1, next_x0, next_x1, triplet=None)
    return z0,z1
    # print(f"z0:{z0},z1:{z1},z0^z1:{z0 ^ z1}")
#
# if __name__ == '__main__':
#
#     for i in range(100000):
#         x0 =[random.randint(0,1) for i in range(2)]
#         x1 =[random.randint(0,1) for i in range(2)]
#         hope_result = (x0[0] ^ x1[0]) and (x0[1] ^ x1[1])
#
#         z0, z1 = bool_bit_and(x0[0], x1[0], x0[1], x1[1], None)
#         if(z0^z1 != hope_result):
#             print('-' * 100)
#             print(f"x0:{x0},x1:{x1},hope_result:{hope_result}")
#             print(f"z0:{z0},z1:{z1},z0^z1:{z0^z1}")

def xor_sum(matrix_a, matrix_b,overlap_count):
    # 将矩阵转换为 numpy 数组
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)

    # 计算每个矩阵中1的个数
    x_a = np.sum(matrix_a)
    x_b = np.sum(matrix_b)

    # 计算重叠的1的个数
    # overlap_count = np.sum(np.logical_and(matrix_a, matrix_b))

    # 计算异或和
    xor_sum_result = x_a + x_b - 2 * overlap_count

    return xor_sum_result

if __name__ == '__main__':
    pad_len = 64
    x1 = ['f1','f2']
    x2 = ['f2','f3']
    # x1 = ['f1','f2','f3','f4','f6']
    # x2 = ['f2','f3','f4','f5','f6']
    print(f"P0输入:{x1}")
    print(f"P1输入:{x2}")
    m = len(x1)
    n = len(x2)
    px1 = np.full((m,n), -1)
    px2 = np.full((m,n), -1)
    for i,v1 in enumerate(x1):
        for j,v2 in enumerate(x2):
            #秘密分享比较两个数是否相等
            z0,z1 = compare_two_item(v1,v2)
            px1[i][j] = z0
            px2[i][j] = z1

    pss1 = []
    pss2 = []
    #秘密分享乘法计算and都为1的个数
    # ss0, ss1 = ss_mul(, )
    for i in range(m):
        for j in range(n):
            item1 = mpz(px1[i][j])
            item2 = mpz(px2[i][j])
            ss0,ss1 = ss_mul(item1,item2,p_len=64)
            pss1.append(ss0)
            pss2.append(ss1)

    px1_sum = np.sum(px1)


    px2_sum = np.sum(px2)

    pss1_sum = np.sum(pss1)
    print(pss1)
    pss2_sum = np.sum(pss2)
    print(pss2)
    overlap_sum = np.sum(pss1) + np.sum(pss2)
    insec_num = px1_sum + px2_sum - 2 * overlap_sum

    print("首先计算布尔比较值")
    print(f"P0结果:{px1_sum}")
    print(px1)
    print(f"P1结果:{px2_sum}")
    print(px2)

    print("两个布尔比较矩阵结果进行秘密分享乘法 获得双方都是1的个数")
    print(f"pss1的和:{pss1_sum}")
    print(f"pss2的和:{pss2_sum}")
    print(f"overlap_sum:{overlap_sum}")
    print(f"P0结果:{px1_sum},P1结果:{px2_sum}")
    print(f"交集个数计算px1_sum+px2_sum - 2*overlap_sum")
    print(f"px1_sum:{px1_sum}+px2_sum:{px2_sum}-2*{overlap_sum} = {insec_num}")
    print(f"最终的交集个数:{insec_num}")




# if __name__ == '__main__':
#     x1 = 'fuck1'
#     x2 = 'fuck2'
#     print("hash 256".center(100,'='))
#     x1_hash = compute_sha256(x1)[:16]
#     x2_hash = compute_sha256(x2)[:16]
#     print(f"x1_hash:{x1_hash}")
#     print(f"x2_hash:{x2_hash}")
#
#     print("hex to bin".center(100, '='))
#     decimal_value1 = int(x1_hash, 16)
#     decimal_value2 = int(x2_hash, 16)
#     decimal_value1_bin = int_to_binary_array(decimal_value1,pad_len)
#     decimal_value2_bin = int_to_binary_array(decimal_value2,pad_len)
#     print(f"decimal_value1:{decimal_value1_bin},{bin_arr_to_num(decimal_value1_bin)}")
#     print(f"decimal_value2:{decimal_value2_bin},{bin_arr_to_num(decimal_value2_bin)}")
#
#     #
#     print("share xor".center(100, '='))
#     x10, x11 = split_xor_list(decimal_value1_bin)
#     x20, x21 = split_xor_list(decimal_value2_bin)
#     print('verify')
#     x10_n = bin_arr_to_num(x10)
#     x11_n = bin_arr_to_num(x11)
#     x20_n = bin_arr_to_num(x20)
#     x21_n = bin_arr_to_num(x21)
#     print(f"x10:{x10},{x10_n},x11:{x11},{x11_n}==decimal_value0:{x10_n ^ x11_n}")
#     print(f"x20:{x20},{x20_n},x21:{x21},{x21_n}==decimal_value1:{x20_n ^ x21_n}")
#     # # decimal_value2 = int(hex_str2, 16)
#     #
#     print("P0方构造步骤".center(100, '='))
#     tmp0_xor = list_xor(x10,x20,pad_len)
#     tmp0_bin = [1^v for v in tmp0_xor]
#     # tmp0_bin = [0, 0]
#     print(f"tmp0_xor:{tmp0_xor}")
#     print(f"tmp0:{tmp0_bin}")
#     #
#     print("P1方构造步骤".center(100, '='))
#     tmp1_bin = list_xor(x11,x21,pad_len)
#     # tmp1_bin=[0,0]
#     print(f"tmp1:{tmp1_bin}")
#
#     # for j in range(100):
#         # #
#     z0 = tmp0_bin[0]
#     z1 = tmp1_bin[0]
#     # triplet = (1, 1, 0),(1, 1, 0)
#     # triplet = generate_boolean_triplet()
#     # print("循环计算".center(100, '='))
#     # print(f"current{1} z0:{z0},z1:{z1},z0^z1:{z0 ^ z1}")
#     for i in range(1,pad_len):
#         next_x0 = tmp0_bin[i]
#         next_x1 = tmp1_bin[i]
#         # print('-'*100)
#         # print(f"cur {i+1},z0:{z0},z1:{z1},x0:{next_x0},x1:{next_x1}")
#         # print(f"hope_result:{(z0^z1) and (next_x0^next_x1)}")
#         z0,z1 = bool_bit_and(z0,z1,next_x0,next_x1,triplet=None)
#         # print(f"current{i+1} z0:{z0},z1:{z1},z0^z1:{z0^z1}")
#     print(f"z0:{z0},z1:{z1},z0^z1:{z0^z1}")
# #
#
#
#     # ===================
#     # print("计算前两位的布尔秘密分享值".center(100, '='))
#     # print('==生成乘法三元组==')
#     # # triplet = generate_boolean_triplet()
#     # (a0, b0, c0), (a1, b1, c1) = triplet
#     # print(f"a0,b0,c0:{(a0, b0, c0)}")
#     # print(f"a1,b1,c1:{(a1, b1, c1)}")
#     # print(f"(a0^a1) and (b0^b1):{(a0^a1) and (b0^b1)},c0^c1:{c0^c1}")
#     #
#     # print("==P0方计算e0和f0,p1方计算e1和f0==")
#     # e0 = a0 ^ tmp0_bin[0]
#     # f0 = b0 ^ tmp0_bin[1]
#     # e1 = a1 ^ tmp1_bin[0]
#     # f1 = b1 ^ tmp1_bin[1]
#     # e = e0^e1
#     # f = f0^f1
#     # print(f"e0:{e0},f0:{f0}")
#     # print(f"e1:{e1},f1:{f1}")
#     # print(f"e:{e},f1:{f}")
#     #
#     #
#     # print("==P0方计算z0_1,p1方计算z0_2==")
#     # z0_1 = (0 and e and f) ^(f and a0) ^(e and b0) ^ c0
#     # z1_1 = (0 and e and f) ^(f and a1) ^(e and b1) ^ c1
#     # print(f"z0_1:{z0_1},z1_1:{z1_1}，z0_1^z1_1:{z0_1^z1_1}")
#
#     # print("计算前三位的布尔秘密分享值".center(100, '='))
#     # print('==生成乘法三元组==')
#     # triplet = generate_boolean_triplet()
#     # (a0, b0, c0), (a1, b1, c1) = triplet
#     # print(f"(a0^a1) ^ (b0^b1):{(a0 ^ a1) ^ (b0 ^ b1)},c0^c1:{c0 ^ c1}")
#     #
#     # print("==P0方计算e0和f0,p1方计算e1和f0==")
#     # e0 = a0 ^ z0_1
#     # f0 = b0 ^ tmp0_bin[2]
#     # e1 = a1 ^ z1_1
#     # f1 = b1 ^ tmp1_bin[2]
#     # e = e0 ^ e1
#     # f = f0 ^ f1
#     # print(f"e0:{e0},f0:{f0}")
#     # print(f"e1:{e1},f1:{f1}")
#     # print(f"e:{e},f1:{f}")
#     #
#     # print("==P0方计算z0_1,p1方计算z0_2==")
#     # z0_2 = (0 ^ e ^ f) ^ (f ^ a0) ^ (e ^ b0) ^ c0
#     # z1_2 = (0 ^ e ^ f) ^ (f ^ a1) ^ (e ^ b1) ^ c1
#     # print(f"z0_2:{z0_2},z1_2:{z1_2}")
#     #
#     # print("计算前四位的布尔秘密分享值".center(100, '='))
#     # print('==生成乘法三元组==')
#     # triplet = generate_boolean_triplet()
#     # (a0, b0, c0), (a1, b1, c1) = triplet
#     # print(f"(a0^a1) ^ (b0^b1):{(a0 ^ a1) ^ (b0 ^ b1)},c0^c1:{c0 ^ c1}")
#     #
#     # print("==P0方计算e0和f0,p1方计算e1和f0==")
#     # e0 = a0 ^ z0_2
#     # f0 = b0 ^ tmp0_bin[3]
#     # e1 = a1 ^ z1_2
#     # f1 = b1 ^ tmp1_bin[3]
#     # e = e0 ^ e1
#     # f = f0 ^ f1
#     # print(f"e0:{e0},f0:{f0}")
#     # print(f"e1:{e1},f1:{f1}")
#     # print(f"e:{e},f1:{f}")
#     #
#     # print("==P0方计算z0_3,p1方计算z1_3==")
#     # z0_3 = (0 ^ e ^ f) ^ (f ^ a0) ^ (e ^ b0) ^ c0
#     # z1_3 = (0 ^ e ^ f) ^ (f ^ a1) ^ (e ^ b1) ^ c1
#     # print(f"z0_3:{z0_3},z1_3:{z1_3}")
#     # pass