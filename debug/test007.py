def check_floodlight_modes(floodlight_config):
    # 模式名称映射
    mode_name_mapping = {
        'night_vision_steady_light': '夜视常亮模式',
        'preview_opens_auto': '预览自动开启',
        'brightness': '亮度',
        'light_off_mode': '关闭',
        'timer_mode': '定时模式',
        'auto_mode': '自动模式',
        'smart_mode': '智能模式',
        'night_smart_mode': '夜间智能模式'
    }

    supported_modes = []
    supported_cn_name = []

    # 检查yaml内容中的每个模式
    for mode in floodlight_config:
        if floodlight_config[mode]:
            supported_modes.append(mode)

            # 转换键名为对应的模式名称
            mode_name = mode_name_mapping.get(mode, mode)
            supported_cn_name.append(mode_name)

    # 输出支持的模式
    if supported_modes:
        print(supported_modes)
        print(supported_cn_name)
    else:
        print("该设备不支持任何模式")


# 示例yaml内容
floodlight_config = {
    'night_vision_steady_light': '夜视常亮模式(有则保留无则删除)',
    'preview_opens_auto': '预览自动开启(有则保留无则删除)',
    'brightness': '亮度(有则保留无则删除)',
    'light_off_mode': '关闭(有则保留无则删除)',
    'timer_mode': '定时模式(有则保留无则删除)',
    'auto_mode': '自动模式(有则保留无则删除)',
    'smart_mode': '智能模式',
    'night_smart_mode': '夜间智能模式'
}

# 调用方法
check_floodlight_modes(floodlight_config)
