
class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)


INSERT_GRPC_SQL = '''
INSERT INTO test.transfer_data
(src_role, dst_role, index_id, fuc_type, trans_data)
VALUES('{}', '{}', '{}', '{}', '{}');
'''


SELECT_GRPC_SQL = '''
SELECT * from test.transfer_data 
WHERE index_id = '{}';
'''

party1_grpc = {
    "ip": "127.0.0.1",
    "port": "10001",
    "protocol": "grpc",
    "role": "party1"
}
party1_grpc = DictToObject(party1_grpc)

party2_grpc = {
    "ip": "127.0.0.1",
    "port": "10002",
    "protocol": "grpc",
    "role": "party2"
}
party2_grpc = DictToObject(party2_grpc)