def traffic_conversion_bytes(traffic_in_bytes: str):
    # 将输入的字符串转换为整数
    traffic_in_bytes = int(traffic_in_bytes.replace('B', '').strip())

    # 换算关系
    bytes_to_kilobytes = 1 / 1024
    bytes_to_megabytes = 1 / (1024 ** 2)
    bytes_to_gigabytes = 1 / (1024 ** 3)
    bytes_to_terabytes = 1 / (1024 ** 4)

    # 换算
    kilobytes = traffic_in_bytes * bytes_to_kilobytes
    megabytes = traffic_in_bytes * bytes_to_megabytes
    gigabytes = traffic_in_bytes * bytes_to_gigabytes
    terabytes = traffic_in_bytes * bytes_to_terabytes

    # 格式化输出
    result = f"""
    输入流量: {traffic_in_bytes}B
    换算结果:
    - 千字节 (KB): {kilobytes:.2f} KB
    - 兆字节 (MB): {megabytes:.2f} MB
    - 吉字节 (GB): {gigabytes:.2f} GB
    - 太字节 (TB): {terabytes:.2f} TB
    """
    print(result)
    return result


# 示例输入
traffic_input_bytes = "524288000B"
traffic_conversion_bytes(traffic_input_bytes)
