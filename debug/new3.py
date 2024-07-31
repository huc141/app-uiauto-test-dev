import os
import pytest
import yaml

# 设备文件夹的根目录
config_root_dir = 'config'

# 获取每个设备文件夹的路径
device_dirs = [os.path.join(config_root_dir, d) for d in os.listdir(config_root_dir) if
               os.path.isdir(os.path.join(config_root_dir, d))]


# 定义一个函数来加载指定设备文件夹中的 YAML 文件
def load_wifi_parse_xml(device_dir):
    yaml_file_path = os.path.join(device_dir, 'wifi_parse_xml.yml')
    with open(yaml_file_path, 'r') as file:
        return yaml.safe_load(file)


# 加载所有设备的 YAML 文件内容
wifi_configs = [load_wifi_parse_xml(device_dir) for device_dir in device_dirs]


# 测试类
class TestAppBehavior:
    @pytest.mark.parametrize("wifi_config", wifi_configs)
    def test_wifi_parse(self, wifi_config):
        # 获取配置参数
        device_name = wifi_config['device_name']
        app_version = wifi_config['app_version']
        expected_result = wifi_config['expected_result']

        # 打印信息，实际测试中可能进行其他操作
        print(f"Testing {device_name} with app version {app_version}")

        # 假设我们有一个函数来执行WiFi解析测试
        actual_result = perform_wifi_parse_test(device_name)

        # 断言测试结果是否与预期相符
        assert actual_result == expected_result, f"Test failed for {device_name}: Expected result {expected_result}, got {actual_result}"


# 假设的辅助函数，用于执行WiFi解析测试
def perform_wifi_parse_test(device_name):
    # 这个函数应该是实际执行WiFi解析测试的逻辑
    # 这里只是返回一个模拟的结果
    return "Success"


# 运行测试
pytest.main()
