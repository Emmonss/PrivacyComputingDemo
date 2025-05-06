import torch
import syft as sy

# 初始化虚拟节点
hook = sy.TorchHook(torch)
alice = sy.VirtualWorker(hook, id="alice")
bob = sy.VirtualWorker(hook, id="bob")
crypto_provider = sy.VirtualWorker(hook, id="crypto_provider")

# 定义要比较的数
a = torch.tensor([5])
b = torch.tensor([5])

# 将数据秘密分享到双方
a_shared = a.share(alice, bob, crypto_provider=crypto_provider)
b_shared = b.share(alice, bob, crypto_provider=crypto_provider)

# 安全计算相等性比较（差值的平方是否为0）
diff = a_shared - b_shared
diff_squared = diff * diff  # 使用MPC乘法协议

# 安全比较结果（0表示相等时需要额外处理，这里简化为取反）
result = (1 - diff_squared).get()  # 实际实现需更严谨的比较协议

print("比较结果（密态）:", result)
