
import grpc
import transfer.grpc_trans.proto.demo_pb2 as demo_pb2
import transfer.grpc_trans.proto.demo_pb2_grpc as demo_pb2_grpc

def run():
    # 本次不使用SSL，所以channel是不安全的
    channel = grpc.insecure_channel('localhost:50054')
    # 客户端实例
    stub = demo_pb2_grpc.GreeterStub(channel)
    # 调用服务端方法
    response = stub.GetDeptUser(demo_pb2.GetDeptUserRequest(dept_id=1, dept_name='dd', uid_list=[1, 2, 3]))
    print(response.user_list)
    print(response.user_map)



if __name__ == '__main__':
    run()