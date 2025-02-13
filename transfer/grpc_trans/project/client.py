
import grpc,pickle
from grpc._cython import cygrpc
import transfer.grpc_trans.proto.mytransfer_pb2_grpc as mytransfer_pb2_grpc
import transfer.grpc_trans.proto.mytransfer_pb2 as mytransfer_pb2


def send(src,dst,data):
    src_role = src.role
    dst_role = dst.role
    id_index = '{}-{}-{}'.format(src_role,dst_role,(int)(datetime.now().timestamp()))
    # 本次不使用SSL，所以channel是不安全的
    channel = grpc.insecure_channel(f'{dst.ip}:{dst.port}')
    # 客户端实例
    stub = mytransfer_pb2_grpc.TransferServiceStub(channel)
    # 调用服务端方法
    response = stub.send_data(mytransfer_pb2.Data(id=id_index, src=src_role, dst=dst_role, data = data))
    print(response.code)
    print(response.message)
    return id_index


def get(src,dst,id_index):
    src_role = src.role
    dst_role = dst.role
    # 本次不使用SSL，所以channel是不安全的
    channel = grpc.insecure_channel(f'{dst.ip}:{dst.port}')
    # 客户端实例
    stub = mytransfer_pb2_grpc.TransferServiceStub(channel)
    response = stub.get_data(mytransfer_pb2.Data(id=id_index, src=src_role, dst=dst_role))
    print(response.code)
    print(response.message)
    # print(response.data.decode(encoding='utf8'))
    return response.data.decode(encoding='utf8')
    pass

from datetime import datetime
if __name__ == '__main__':
    # print()
    from transfer.grpc_trans.utils.sql_constant import *

    data_party1 = "data party1 to party2".encode(encoding='utf8')
    data_party2 = "data party2 to party1".encode(encoding='utf8')

    #
    print('='*100)
    party1_party2_data_index = send(party1_grpc, party2_grpc, data_party1)
    print('=' * 100)
    party2_party1_data_index = send(party2_grpc, party1_grpc, data_party2)

    # id_index = "src_party-dst_party-1739330375"
    print('=' * 100)
    get_data_party1 = get(party1_grpc, party2_grpc, party1_party2_data_index)
    print(get_data_party1)
    print('=' * 100)
    get_data_party2 = get(party2_grpc, party1_grpc, party2_party1_data_index)
    print(get_data_party2)
    pass