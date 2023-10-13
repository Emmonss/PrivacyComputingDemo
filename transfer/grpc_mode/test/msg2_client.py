import grpc, sys,time
sys.path.append('/Users/peizhengmeng/code/python/PrivacyComputingDemo')

from transfer.grpc_mode.test.pb import msg2_pb2_grpc,msg2_pb2


def run():
    # 本次不使用SSL，所以channel是不安全的
    channel = grpc.insecure_channel('localhost:50054')
    # 客户端实例
    stub = msg2_pb2_grpc.GreeterStub(channel)

    response = stub.GetDeptUser(msg2_pb2.GetDeptUserRequest(dept_id=1, dept_name='aa', uid_list=[1, 2, 3]))
    print(response.user_list)
    print(response.user_map)


if __name__ == '__main__':
    run()