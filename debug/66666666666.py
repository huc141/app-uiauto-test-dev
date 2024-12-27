import requests
import json

# LogUtil和StepType在Python中不需要，可以直接打印日志
# 一个配置字典来代替androidStepHandler.globalParams
config = {
    "api_server": "http://192.168.100.159:8002",
    "is_default": True,
    "username": "admin",
    "password": "reolink123",
    "device_uid": "952700Y005K15KA1",
    "ip": "192.168.1.1",
    "api_params": {"cmd": "getAbility", "channel": 0, "token": 0},
    "api_path": "/ability/getAbility"
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
        print(f"Token: {config['api_token']}")
    else:
        print(f"Failed to get token: {response.status_code}")


t_rest_api_1()


def t_rest_api_2():
    json_data = config["api_params"]
    json_data["token"] = config["api_token"]
    url = f"{config['api_server']}{config['api_path']}"

    headers = {
        "Content-Type": "application/json",
        "SonicToken": "xxxxxxx"
    }

    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    if response.status_code == 200:
        config["api_response"] = response.json()
        print(f"REST API Result: {config['api_response']}")
    else:
        print(f"Failed to get API data: {response.status_code}")


t_rest_api_2()

