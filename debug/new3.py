import os
import pytest
import yaml

# 设备文件夹的根目录
config_root_dir = 'H:\\app-uiauto-test-dev\\config'


# 定义一个函数来加载指定设备文件夹中的 YAML 文件
def load_device_config(device_dir=None, yaml_file_name='setting.yaml'):
    if device_dir is None:
        device_dirs = [os.path.join(config_root_dir, d) for d in os.listdir(config_root_dir) if
                       os.path.isdir(os.path.join(config_root_dir, d))]
    else:
        device_dirs = [os.path.join(config_root_dir, device_dir)]

    device_configs = []
    for _dir in device_dirs:
        yaml_path = os.path.join(_dir, yaml_file_name)
        if os.path.exists(yaml_path):
            try:
                with open(yaml_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                    device_configs.append(config)
            except Exception as e:
                print(f"Warning: {yaml_path} does not exist in {_dir}")
                print(f"Error loading {yaml_path}: {e}")

    return device_configs


devices_config = load_device_config()
print(devices_config)
