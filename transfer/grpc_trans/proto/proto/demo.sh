#python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/demo.proto
#
#python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/helloworld.proto

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mytransfer.proto

#python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/sqllite.proto

