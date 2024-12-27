import requests
import json

# LogUtil和StepType在Python中不需要，可以直接打印日志
# 一个配置字典来代替androidStepHandler.globalParams
config = {
    "api_server": "http://192.168.100.159:8002",
    "is_default": True,
    "username": "admin",
    "password": "reolink123",
    "device_uid": "952700Y006U21XKV",
    "ip": "192.168.1.1",
    "api_path": "/light/getLightCfg",
    "api_params": {"cmd": "getLightCfg", "channel": 0}
}


def t_rest_api_1():
    server = config["api_server"]
    is_use_uid = config["is_default"]
    username = config["username"]
    password = config["password"]
    url = f"{server}/user_uid/login_uid?username={username}&password={password}&name=dev"

    if is_use_uid:
        uid = config["device_uid"]
        url += f"&uid={uid}"
    else:
        ip = config["ip"]
        url = f"{server}/user/login?username={username}&password={password}&host={ip}&name=dev"

    response = requests.get(url)
    result = response.json()

    if response.status_code == 200:
        config["api_token"] = result["token"]
        assert result["code"] == 1
        print(f"API Result: {result}")
        print(f'config: {config}')
        print(f"Token: {config['api_token']}")
    else:
        print(f"Failed to get token: {response.status_code}")


def t_rest_api_2():
    json_data = config["api_params"]
    json_data["token"] = config["api_token"]
    url = f"{config['api_server']}{config['api_path']}"
    print(f"URL: {url}")

    headers = {
        "Content-Type": "application/json",
        "SonicToken": "xxxxxxx"
    }
    # 打印出请求参数
    print(f"Request Data: {json_data}")

    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    if response.status_code == 200:
        config["api_response"] = response.json()
        print(f"REST API Result: {config['api_response']}")
    else:
        print(f"Failed to get API data: {response.status_code}")


t_rest_api_1()
t_rest_api_2()

# 请求数据：
API Result: {'code': 1, 'msg': '登录成功', 'token': 2}
config: {'api_server': 'http://192.168.100.159:8002', 'is_default': True, 'username': 'admin', 'password': 'reolink123', 'device_uid': '952700Y006U21XKV', 'ip': '192.168.1.1', 'api_path': '/light/getLightCfg', 'api_params': {'cmd': 'getLightCfg', 'channel': 0}, 'api_token': 2}
Token: 2
URL: http://192.168.100.159:8002/light/getLightCfg
Request Data: {'cmd': 'getLightCfg', 'channel': 0, 'token': 2}
REST API Result: {'cmd': 'getLightCfg', 'cmdIdx': 0, 'channel': 0, 'channelType': 0, 'device': 1000002, 'statusInfo': {'code': 0, 'message': 'OK'}, 'value': {'irLight': {'state': 'auto'}, 'powerLight': {'state': 'open'}, 'doorbellLight': {'state': 'close'}}, 'range': {'irLight': {'state': ['auto', 'close']}, 'powerLight': {'state': ['close', 'open']}, 'doorbellLight': {'state': ['close', 'open', 'keepOff']}}}