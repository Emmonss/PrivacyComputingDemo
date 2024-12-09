# hello_client.py

import grpc

from transfer.grpc_trans.pyproto import helloworld_pb2, helloworld_pb2_grpc


def run():
    # 本次不使用SSL，所以channel是不安全的
    channel = grpc.insecure_channel('localhost:50054')
    # 客户端实例
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    # 调用服务端方法
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='World'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()