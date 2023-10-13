

from utils.common_utils import check_port
from transfer.grpc_mode import grpc_transfer_pb2_grpc as pb2_grpc
from transfer.grpc_mode import grpc_transfer_pb2 as pb2


import grpc,ipaddress,socket


def get_grpc_addr(ip:str, port:str):
    if ip.startswith("http://"):
        ip = ip.lstrip("http://")
    if ip.startswith("https://"):
        ip = ip.lstrip("https://")

    ip = socket.gethostbyname(ip)
    ipaddress.ip_address(ip)
    check_port(port)

    return ip+":"+port


def init_channel(addr):
    channel = grpc.insecure_channel(target=addr,
                                    options=[('grpc.max_send_message_length',-1),
                                             ('grpc.max_receive_message_length',-1)],
                                    compression=grpc.Compression.Gzip)
    return channel

def send_message(addr,bytes_data,task_id,src_party_id,dst_party_id,name):
    channel = init_channel(addr)
    # channel = grpc.insecure_channel(addr)
    stub = pb2_grpc.DataTransferStub(channel)
    request = pb2.RequestData(bytes_data=bytes_data,
                           task_id=task_id,
                           src_party_id=src_party_id,
                           dst_party_id=dst_party_id,
                           name=name)
    res = stub.grpcDataRemote(request)
    print(res)
    channel.close()

    return res

def get_message(addr,task_id,src_party_id,dst_party_id,name):
    channel = init_channel(addr)
    stub = pb2_grpc.DataTransferStub(channel)
    request = pb2.RequestData(bytes_data=None,
                              task_id=task_id,
                              src_party_id=src_party_id,
                              dst_party_id=dst_party_id,
                              name=name)
    res = stub.grpcDataGet(request)
    channel.close()
    return res

if __name__ == '__main__':
    pass
    addr = get_grpc_addr("localhost","50054")
    # addr = 'localhost:50054'
    data = bytes("fuck".encode())
    task_id = "test_01"
    src_party_id = 101
    dst_party_id = 102
    send_message(addr=addr,
                 bytes_data=data,
                 task_id=task_id,
                 src_party_id=src_party_id,
                 dst_party_id=dst_party_id,
                 name="test")

    res = get_message(addr=addr,
                 task_id=task_id,
                 src_party_id=src_party_id,
                 dst_party_id=dst_party_id,
                 name="test")

    print(res)

    print(res.data.decode())
