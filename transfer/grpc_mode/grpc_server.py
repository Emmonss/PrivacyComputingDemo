from concurrent import futures
import grpc, sys,os,random
sys.path.append('/Users/peizhengmeng/code/python/PrivacyComputingDemo')

from transfer.grpc_mode import grpc_transfer_pb2,grpc_transfer_pb2_grpc
from utils.common_utils import get_data_party_dir,write_bytes_to_file,load_bytes_from_file
from utils.constant_utils import GRPC_PORT

class grpcTransferServer(grpc_transfer_pb2_grpc.DataTransferServicer):
    def grpcDataRemote(self, request, context):
        data = request.bytes_data
        task_id = request.task_id
        src_party_id = request.src_party_id
        dst_party_id = request.dst_party_id
        name = request.name
        try:
            save_dir = get_data_party_dir(task_id, src_party_id, dst_party_id)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            write_bytes_to_file(data, os.path.join(save_dir, name + ".pkl"))

            return grpc_transfer_pb2.ResponseData(code=200,
                                                  message="remote data have been succesfuly saved ")
        except Exception as e:
            return grpc_transfer_pb2.ResponseData(code=500,
                                                  message=f"remote data saved failed by:{e}")

        pass

    def grpcDataGet(self, request, context):
        task_id = request.task_id
        src_party_id = request.src_party_id
        dst_party_id = request.dst_party_id
        name = request.name

        try:
            data_dir = get_data_party_dir(task_id, src_party_id, dst_party_id)
            data_path = os.path.join(data_dir, name + ".pkl")
            if os.path.exists(data_path):
                data = load_bytes_from_file(data_path)
                return grpc_transfer_pb2.ResponseData(data=data,
                                                      code=200,
                                                      message=f"get data from remote server sucess")

            else:
                return grpc_transfer_pb2.ResponseData(code=401,
                                                      message=f"get data from remote server not exist")


        except Exception as e:
            return grpc_transfer_pb2.ResponseData(code=500,
                                                  message=f"get data from remote server failed by:{e}")
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 绑定处理器
    grpc_transfer_pb2_grpc.add_DataTransferServicer_to_server(grpcTransferServer(), server)

    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f'gRPC 服务端已开启，端口为{GRPC_PORT}...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()