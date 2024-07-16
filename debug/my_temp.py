import os
import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET

from common_tools.logger import logger


def parse_and_extract_text(xml_content, exclude_texts=None):
    """
    解析并提取XML指定文本内容，必要时候，你可能需要更新当前方法的解析条件。
    :param xml_content: 获取的xml内容
    :param package: 解析条件
    :param class_name: 解析条件
    :param index: 解析条件
    :param exclude_texts: 需要排除的文本
    :return:
    """
    if exclude_texts is None:
        exclude_texts = []

    texts = set()

    root = ET.fromstring(xml_content)
    for elem in root.iter():
        if (elem.attrib.get('package') == "com.mcu.reolink" and
                elem.attrib.get('class') == "android.widget.TextView" and
                elem.attrib.get('index') == "0" and
                elem.attrib.get('text') != "" and
                elem.attrib.get('resource-id') != 'com.mcu.reolink:id/device_name_tv' and
                elem.attrib.get('enabled') == "true"):
            text = elem.attrib.get('text')
            if text and text not in exclude_texts:
                texts.add(text)

    return texts


def get_all_elements_texts1(driver, exclude_texts, max_scrolls=2, scroll_pause=1):
    """
    获取当前页面的所有元素的text文本内容，并将去重后的XML内容写入文件
    :param driver: uiautomator2的Device对象
    :param max_scrolls: 最大滚动次数
    :param scroll_pause: 滚动后的暂停时间
    :return: 文本内容列表
    """
    all_texts = set()

    for _ in range(max_scrolls):
        # 获取页面的 XML 结构
        page_source = driver.dump_hierarchy()
        logger.info("已获取页面XML")

        # 解析XML并提取指定的文本内容
        texts = parse_and_extract_text(
            page_source,
            exclude_texts=exclude_texts
        )
        all_texts.update(texts)

        # 滑动屏幕
        driver.swipe_ext("up")
        time.sleep(scroll_pause)  # 等待页面稳定

    # 将去重后的文本内容写入文件
    output_path = os.path.abspath("../elements_texts.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        for text in sorted(all_texts):
            f.write(text + '\n')

    # 统计非空行数
    with open(output_path, 'r', encoding='utf-8') as f:
        non_empty_lines = sum(1 for line in f if line.strip())

    print(f"总非空行数: {non_empty_lines}")

    return list(all_texts)


def verify_page_text(expected_text, exclude_texts):
    # 获取页面所有功能名称
    texts = get_all_elements_texts1(expected_text, exclude_texts)

    # file_path = os.path.abspath("../elements_texts.txt")

    # 读取elements_texts.txt文件的页面功能：
    # with open(file_path, 'r', encoding='utf-8') as file2:
    #     file2_content = file2.readlines()

    # 计算当前页面获取到的功能数量
    page_fun_num = len(texts)
    print(f"当前页面获取到的功能数量：{page_fun_num}")

    # 计算预期设备的预期页面的预期文案数量
    count = len(expected_text)
    logger.info(f"预期设备的预期页面的预期文案数量：{count}")

    for line in expected_text:
        if line not in texts or page_fun_num != count:
            logger.info("功能可能不齐全！需要人工核查！")
            return False
    logger.info("功能比对齐全！")
    return True


# 使用示例
if __name__ == "__main__":
    driver = u2.connect_usb("28131FDH2000K1")
    exclude_texts = ["开", "关", "设置", "报警设置", "报警通知", "更多", "0", "退出登录设备", "删除", "布防",
                     "通道"]
    texts = get_all_elements_texts1(driver, exclude_texts)
    print(f"共获取到 {len(texts)} 个唯一的文本内容")
