from transfer.grpc_trans.utils.sql_constant import party2_grpc
from transfer.grpc_trans.project.server import serve



if __name__ == '__main__':
    #type part2 port:100002
    serve(party2_grpc.port)