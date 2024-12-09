
import grpc,pickle
from grpc._cython import cygrpc
import transfer.grpc_trans.proto.mytransfer_pb2_grpc as mytransfer_pb2_grpc
import transfer.grpc_trans.proto.mytransfer_pb2 as mytransfer_pb2
#grpc_trans 传输最大数据包：2G
grpc_max_data_size = 2147483647
#grpc_trans 传输超时时间
grpc_time_out = 60*60*48

grpc_retry_times = 3

grpc_retry_interval_time = 20

ssl_common_name = "grpc-target"


def build_message(src_role,dst_role,data):
    length = len(data)
    cursor = 10
    end = 0
    while (end<length):
        start = end
        end+= cursor
        yield mytransfer_pb2.Data(id="1",src = src_role,
                                  dst = dst_role,data=data[start:end])
    pass

def send(src, dst, data, timout=10):
    channel,stub = init_transfer_channel(dst)
    success = False
    cursor = 0
    result = dict()

    src_role = src.get("role")
    dst_role = src.get("role")
    while not success and cursor< grpc_retry_times:
        try:
            response = stub.send_data(
                build_message(src_role, dst_role, data))
            result[dst_role] = response
        except Exception as e:
            print(e)
        cursor+=1
    pass


def init_transfer_channel(info):
    dst_ip = info.get("ip")
    dst_port = info.get("port")
    protocol = info.get("protocol")

    target = "{}:{}".format(dst_ip,dst_port)
    #insecure
    channel = grpc.insecure_channel(target=target,
        options=[(cygrpc.ChannelArgKey.max_send_message_length, grpc_max_data_size),
                 (cygrpc.ChannelArgKey.max_receive_message_length,grpc_max_data_size),
                 ("grpc.ssl_target_name_override", ssl_common_name)
                ])
    stub = mytransfer_pb2_grpc.TransferServiceStub(channel)
    return channel,stub

if __name__ == '__main__':
    src ={
        "ip":"127.0.0.1",
        "port":"10001",
        "protocol":"grpc",
        "role":"src_party"
    }

    dst = {
        "ip": "127.0.0.1",
        "port": "10002",
        "protocol": "grpc",
        "role": "dst_party"
    }

    data = "test_str123123123123123123123123123"
    data = data.encode(encoding='utf8')

    send(src, dst, data, timout=10)
    # channel,stub = init_transfer_channel(info)
    # print(channel)
    # print(stub)
    pass