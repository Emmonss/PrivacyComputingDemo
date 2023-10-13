from concurrent import futures
import grpc, sys,random
sys.path.append('/Users/peizhengmeng/code/python/PrivacyComputingDemo')

from transfer.grpc_mode.test.pb import msg2_pb2_grpc,msg2_pb2


# 实现定义的方法
class Greeter(msg2_pb2_grpc.GreeterServicer):
    def GetDeptUser(self, request, context):
        # 字段使用点号获取
        dept_id = request.dept_id
        dept_name = request.dept_name
        uid_list = request.uid_list
        if dept_id <= 0 or dept_name == '' or len(uid_list) <= 0:
            return msg2_pb2.GetDeptUserResponse()
        print('dept_id is {0}, dept_name is {1}'.format(dept_id, dept_name))
        user_list = []
        user_map = {}
        for id_ in uid_list:
            uid = id_ + random.randint(0, 1000)
            letters = 'qwertyuiopasdfghjklzxcvbnm'
            name = "".join(random.sample(letters, 10))
            user = msg2_pb2.BasicUser()
            user.id = uid
            user.name = name
            user_list.append(user) # 与正常的添加操作差不多
            user_map[uid] = user
        return msg2_pb2.GetDeptUserResponse(user_list=user_list, user_map=user_map)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 绑定处理器
    msg2_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    server.add_insecure_port('[::]:50054')
    server.start()
    print('gRPC 服务端已开启，端口为50054...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()