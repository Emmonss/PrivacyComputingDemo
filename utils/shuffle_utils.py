import random

def shuffle_with_seed(data, seed):
    """根据指定的种子打乱列表，并返回打乱后的列表和索引映射"""
    random.seed(seed)  # 设置随机种子
    indices = list(range(len(data)))  # 记录原始索引
    random.shuffle(indices)  # 打乱索引
    shuffled = [data[i] for i in indices]  # 根据打乱的索引重新排列数据
    return shuffled, indices

def restore_with_indices(shuffled, indices):
    """根据索引映射恢复原始列表"""
    restored = [None] * len(shuffled)
    for i, original_index in enumerate(indices):
        restored[original_index] = shuffled[i]
    return restored

def find_index(lst, value):
    try:
        return lst.index(value)
    except ValueError:
        return -1