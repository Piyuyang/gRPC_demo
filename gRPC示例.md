# gRPC示例
以两数求和为例

#### 第一步：使用Protocol Buffers（proto3）的IDL接口定义语言定义接口服务，编写在文本文件（以.proto为后缀名）中

```
// 注释为双斜线，该文件名为demo.proto
// synax声明版本，默认为版本2
syntax = 'proto3';

// 函数参数、函数返回值都是一个一个消息类型，对应于python中的类

message AddRequest {
//    参数类型 参数名字 参数编号;
    int32 num1=1;
    int32 num2=2;
}

message AddResponse {
    int32 reply=1;
}

// 使用service定义RPC服务，一个service中可以定义多个方法

service AddService {
//      rpc 方法名 (参数message) returns (返回值message) {}
    rpc AddFunc (AddRequest) returns (AddResponse) {}
}
```

#### 第二步：使用gRPC protobuf生成工具生成对应的辅助代码模块

```
python -m grpc_tools.protoc -I=搜索proto文件中被导入文件的目录 --python_out=保存生成py文件的目录 --grpc_python_out=保存生成py文件的目录 上一步编写的proto文件路径
```

--python_out 生成的文件包含接口定义中的数据类型

--grpc_python_out 生成的文件中包含接口定义中的服务类型

#### 第三步：编写gRPC server端代码

```
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
# 通过thread pool来并发处理server的任务
server = grpc.server(ThreadPoolExecutor(10))

# 绑定IP地址，端口号
# 使用的非安全接口，世界gRPC支持TLS/SSL安全连接，以及各种鉴权机制
server.add_insecure_port('127.0.0.1:8888')

# 为服务器注册被调用的函数，第一个参数为servicer类的实例
demo_pb2_grpc.add_AddServiceServicer_to_server(AddServiceServicer(), server)

# 启动服务器
server.start()  # 非阻塞的

# 为防止程序退出，手动阻塞
while True:
    sleep(10)

```

#### 第四步：编写gRPC client端代码

```
import grpc

import demo_pb2
import demo_pb2_grpc

# 创建与服务器的链接，使用with语法保证ch自动关闭
with grpc.insecure_channel('127.0.0.1:8888') as ch:
    
    # 创建stub对象，客户端通过stub来实现rpc通信
    stub = demo_pb2_grpc.AddServiceStub(ch)

    # 创建参数对象
    params = demo_pb2.AddRequest()
    params.num1 = 100
    params.num2 = 200

    # 执行函数
    ret = stub.AddFunc(params).reply

    print(ret)
```













