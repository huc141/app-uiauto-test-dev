import time
import uiautomator2 as u2
import xml.etree.ElementTree as ET


def get_all_elements_texts(driver, max_scrolls=2, scroll_pause=1):
    """
    获取当前页面的所有元素的text文本内容
    :param scroll_pause:
    :param max_scrolls:
    :param driver: uiautomator2的Device对象
    :return: 文本内容列表
    """
    texts = set()

    for _ in range(max_scrolls):
        # 获取页面的 XML 结构
        page_source = driver.dump_hierarchy()
        print(page_source)

        # 解析 XML 并提取所有元素的文本内容
        root = ET.fromstring(page_source)
        print(root)

        with open('destination.xml', 'w', encoding='utf-8') as destination_file:
            destination_file.write(page_source)

        def parse_element(element):
            text = element.attrib.get('text', '').strip()
            if text:
                texts.add(text)
            for child in element:
                parse_element(child)

        parse_element(root)

        # 滑动屏幕
        driver.swipe_ext("up")
        time.sleep(scroll_pause)  # 等待页面稳定

    return list(texts)


if __name__ == "__main__":
    driver = u2.connect_usb("28131FDH2000K1")
    texts = get_all_elements_texts(driver, max_scrolls=2)
