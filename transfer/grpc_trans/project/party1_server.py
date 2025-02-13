

from transfer.grpc_trans.utils.sql_constant import party1_grpc
from transfer.grpc_trans.project.server import serve



if __name__ == '__main__':
    #type part1 port:100001
    serve(party1_grpc.port)