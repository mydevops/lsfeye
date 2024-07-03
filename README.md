<div align="center">
    <h1>lsfeye</h1>
    <img src="./docs/logo/lsfeye.png" width="200" alt=""/>
    <p align="center">
        Monitoring system for IBM LSF
    </p>
</div>

<br>

**当前项目处于测试阶段。**

## 概述
`lsfeye`是一个简单的`LSF`监控系统。核心设计逻辑是通过`LSF`提供的命令进行定时收集并存储至数据库。开放通用的`API`接口，通过标准的`SQL`语句进行查询。

`lsfeye`是免费软件，根据`MIT`许可证发布。

## 安装
下载完成后进入`lsfeye`目录执行。
```shell
make build
```
执行完成后会在`.build_tmp`目录下生成`lsfeye`二进制可执行文件。

## 配置
默认存储在`etc/lsfeye.confg`

### 基础配置
```
[BASIC]
app_name = lsfeye  # 应用名称
host = 0.0.0.0     # 监听的 IP 地址
port = 8000        # 监听的端口号
workers_count = 2  # 进程数量
debug = true       # 是否开启 debug 模式
```

### 日志配置
```
[LOGURU]
path = /opt/log/lsfeye  # 日志存放目录
filename = lsfeye.log   # 日志文件名称
level = info            # 日志保存级别
rotation = 500 MB       # 切分阈值
format = <level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>  # 日志格式
```

### 数据库配置
`lsfeye`数据库需要提前创建，表结构不需要。
```
[MYSQL]
scheme = mysql+aiomysql  # 协议
host = 127.0.0.1         # 连接地址
port = 3306              # 连接端口
user = root              # 用户名
password = 111qqq```     # 密码
db = lsfeye              # 库名
```

### 锁配置
由于涉及到多进程运行，为了避免竞争，采用端口占用的方式来加锁。
```
[SCHEDULERLOCK]
host = 127.0.0.1  # 监听 IP
port = 8001       # 监听端口
```

### 频次控制
```
[INTERVALTRIGGER]  // unit: Seconds
bqueues = 10  # 每 10 秒运行一次
```
