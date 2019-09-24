import grpc

import demo_pb2
import demo_pb2_grpc

# 创建与服务器的链接
with grpc.insecure_channel('127.0.0.1:8888') as conn:
    # 创建调用的服务对象
    stub = demo_pb2_grpc.AddServiceStub(conn)

    # 创建参数对象
    params = demo_pb2.AddRequest()
    params.num1 = 100
    params.num2 = 200

    # 执行函数
    ret = stub.AddFunc(params).reply

    print(ret)
