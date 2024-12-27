import requests
import json
from common_tools.read_yaml import read_yaml
api_config = read_yaml.get_data(key="api_config", source="global_data")   # 读取全局配置

print(api_config)


def get_device_token(uid):
    server = api_config["api_server"]
    is_use_uid = api_config["is_default"]
    username = api_config["username"]
    password = api_config["password"]
    url = f"{server}/5688389-5369357-default/249356636?username={username}&password={password}&name=dev"

    if is_use_uid:
        device_uid = uid
        url += f"&uid={device_uid}"
    else:
        ip = api_config["ip"]
        url = f"{server}/5688389-5369357-default/249356636?username={username}&password={password}&host={ip}&name=dev"

    response = requests.get(url)
    print(f"Request URL: {url}")
    result = response.json()

    if response.status_code == 200:
        api_config["api_token"] = result["token"]
        assert result["code"] == 1
        print(f"API Result: {result}")
        print(f'config: {api_config}')
        print(f"Token: {api_config['api_token']}")
    else:
        print(f"Failed to get token: {response.status_code}")


get_device_token(uid='952700Y006U21XKV')


def get_device_info(api_path, api_params, token):
    pass

