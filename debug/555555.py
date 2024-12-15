from common_tools.read_yaml import read_yaml

g_config = read_yaml.read_global_data(source="global_data")   # 读取全局配置

_access_mode = g_config.get('access_mode')  # 设备接入方式
_nvr_name = g_config.get('nvr_name')  # nvr名称
_hub_name = g_config.get('hub_name')  # hub名称

print(_access_mode)
print(_nvr_name)
print(_hub_name)