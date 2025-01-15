import os
import yaml


def search_and_replace_yaml(folder_path, search_str, replace_str, replace=False):
    """
    遍历文件夹及子文件夹中的yaml文件，查找并替换指定内容。

    :param folder_path: 目标文件夹路径
    :param search_str: 需要查找的字符串
    :param replace_str: 需要替换的字符串
    :param replace: 是否进行替换，True：替换，False：仅查找
    """
    # 遍历文件夹及子文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 只处理yaml文件
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # 读取YAML文件内容
                        content = yaml.safe_load(f)

                    # 检查文件中是否存在需要查找的字符串
                    if find_in_yaml(content, search_str):
                        print(f"找到匹配内容的文件: {file_path}")

                        # 如果需要替换，执行替换操作
                        if replace:
                            updated_content = replace_in_yaml(content, search_str, replace_str)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                # 写入替换后的内容
                                yaml.dump(updated_content, f, allow_unicode=True)
                            print(f"已替换文件: {file_path}")

                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")


def find_in_yaml(data, search_str):
    """
    在YAML数据中查找指定字符串。

    :param data: YAML数据
    :param search_str: 需要查找的字符串
    :return: 如果找到返回True，否则返回False
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if find_in_yaml(value, search_str):
                return True
    elif isinstance(data, list):
        for item in data:
            if find_in_yaml(item, search_str):
                return True
    elif isinstance(data, str):
        if search_str in data:
            return True
    return False


def replace_in_yaml(data, search_str, replace_str):
    """
    替换YAML数据中的指定字符串。

    :param data: YAML数据
    :param search_str: 需要查找的字符串
    :param replace_str: 替换成的新字符串
    :return: 替换后的YAML数据
    """
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_in_yaml(value, search_str, replace_str)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = replace_in_yaml(item, search_str, replace_str)
    elif isinstance(data, str):
        data = data.replace(search_str, replace_str)
    return data


# 示例调用
folder_path = 'D:/app-uiauto-test-dev/config/power-63-2'  # 替换为实际文件夹路径
search_str = '日夜切换阈值'  # 需要查找的字符串
replace_str = '日夜切换阈值'  # 需要替换的字符串
replace = False  # 设置为True进行替换，False则仅查找

search_and_replace_yaml(folder_path, search_str, replace_str, replace)
