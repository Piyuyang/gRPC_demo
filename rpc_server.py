from concurrent.futures import ThreadPoolExecutor
from time import sleep

import grpc

import demo_pb2
import demo_pb2_grpc


class AddServiceServicer(demo_pb2_grpc.AddServiceServicer):
    """重写rpc服务器类"""

    def AddFunc(self, request, context):
        """
        重写add方法
        :param request: 请求参数类，即proto文件中AddRequest
        :param context: 定义状态码、状态详情的工具类
        :return:
        """
        num1 = request.num1
        num2 = request.num2

        # 构建响应类，即proto文件中的AddResponse
        response = demo_pb2.AddResponse()
        response.reply = num1 + num2
        return response


# 创建服务器
server = grpc.server(ThreadPoolExecutor(10))

# 绑定IP地址，端口号
server.add_insecure_port('127.0.0.1:8888')

# 为服务器注册被调用的函数
demo_pb2_grpc.add_AddServiceServicer_to_server(AddServiceServicer(), server)

# 启动服务器
server.start()  # 非阻塞的

# 为防止程序退出，手动阻塞
while True:
    sleep(10)
