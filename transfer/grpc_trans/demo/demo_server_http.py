import random
import flask
from flask import request
import demo_pb2, demo_pb2_grpc

app = flask.Flask(__name__)


@app.route('/get_dept_user', methods=['POST'])
def get_dept_user():
    # 接收client数据并进行反序列化
    req_data = request.data
    user_req = demo_pb2.GetDeptUserRequest()
    user_req.ParseFromString(req_data)

    # 拼接响应信息
    dept_id = user_req.dept_id
    dept_name = user_req.dept_name
    print('dept_id is {0}, dept_name is {1}'.format(dept_id, dept_name))
    uid_list = user_req.uid_list
    user_list = []
    for id_ in uid_list:
        uid = id_ + random.randint(0, 1000)
        letters = 'qwertyuiopasdfghjklzxcvbnm'
        name = "".join(random.sample(letters, 10))
        user = demo_pb2.BasicUser()
        user.id = uid
        user.name = name
        user_list.append(user)
    # 将响应信息序列化
    rsp = demo_pb2.GetDeptUserResponse()
    rsp.user_list.extend(user_list)
    rsp_data = rsp.SerializeToString()
    return rsp_data


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)