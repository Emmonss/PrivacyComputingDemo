import numpy as np


def xor_sum(matrix_a, matrix_b):
    # 将矩阵转换为 numpy 数组
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)

    # 计算每个矩阵中1的个数
    x_a = np.sum(matrix_a)
    x_b = np.sum(matrix_b)

    # 计算重叠的1的个数
    overlap_count = np.sum(np.logical_and(matrix_a, matrix_b))

    # 计算异或和
    xor_sum_result = x_a + x_b - 2 * overlap_count

    return xor_sum_result

if __name__ == '__main__':

    # 示例矩阵
    matrix_a = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 1, 0]
    ]

    matrix_b = [
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 1]
    ]

    result = xor_sum(matrix_a, matrix_b)
    print("异或和:", result)
