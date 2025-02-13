import transfer.grpc_trans.proto.mytransfer_pb2_grpc as mytransfer_pb2_grpc
import transfer.grpc_trans.proto.mytransfer_pb2 as mytransfer_pb2
import grpc
from concurrent import futures
from transfer.grpc_trans.utils.util_mysql import *
from transfer.grpc_trans.utils.sql_constant import *
conn_dict = {
        "host" : '121.5.153.102',
        "database" : 'test',
        "user" : 'root',
        "password" : 'pzmabc123'
    }
conn_dict = DictToObject(conn_dict)
class TransferServer(mytransfer_pb2_grpc.TransferServiceServicer):
    def send_data(self, request, context):
        sql_conn = MySQLConn(conn_dict)
        src_role = request.src
        dst_role = request.dst
        index_id = request.id
        fuc_type = "send gprc"
        data = request.data
        trans_data = data.decode(encoding='utf8')
        sql = INSERT_GRPC_SQL.format(src_role, dst_role, index_id, fuc_type, trans_data)
        print(sql)
        if sql_conn.conn is None or not sql_conn.conn.is_connected():
            return mytransfer_pb2.Response(code="402",message=f"数据库初始化失败",data=None)
        try:
            sql_conn.cursor.execute(sql)
            sql_conn.conn.commit()
            print(f"success saved data from:{src_role} dst:{dst_role}")
            sql_conn.close()
            return mytransfer_pb2.Response(code="200",
                message=f"success saved data from:{src_role} dst:{dst_role}",data=None)
        except Exception as e:
            print(e)
            sql_conn.close()
            return mytransfer_pb2.Response(code="401",message=f"save data by grpc failed",data=None)

    def get_data(self, request, context):
        sql_conn = MySQLConn(conn_dict)
        index_id = request.id
        src_role = request.src
        dst_role = request.dst
        sql = SELECT_GRPC_SQL.format(index_id)
        res_data = ""
        if sql_conn.conn is None or not sql_conn.conn.is_connected():
            return mytransfer_pb2.Response(code="402",message=f"数据库初始化失败",data=None)
        try:
            sql_conn.cursor.execute(sql)
            results = sql_conn.cursor.fetchall()
            if len(results)==0:
                return mytransfer_pb2.Response(code="403",
                        message=f"get none data from:{dst_role}", data=None)
            for item in results:
                if src_role!=item[1] or dst_role != item[2]:
                    return mytransfer_pb2.Response(code="403",
                        message=f"the role of src and dst is not same:{dst_role}", data=None)
                else:
                    res_data += item[5]
            print(f"success get data from:{src_role} dst:{dst_role}")
            sql_conn.close()
            return mytransfer_pb2.Response(code="200",
                message=f"success get data from party:{dst_role}",data=res_data.encode(encoding='utf8'))
        except Exception as e:
            print(e)
            sql_conn.close()
            return mytransfer_pb2.Response(code="401",message=f"get data by grpc failed",data=None)



def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 绑定处理器
    mytransfer_pb2_grpc.add_TransferServiceServicer_to_server(TransferServer(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'gRPC 服务端已开启，端口为{port}...')
    server.wait_for_termination()

if __name__ == '__main__':
    from transfer.grpc_trans.utils.sql_constant import party1_grpc
    serve(party1_grpc.port)
