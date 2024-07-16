import xml.etree.ElementTree as ET


def parse_and_extract_text(xml_path, output_path, package, class_name, index, exclude_texts=None):
    if exclude_texts is None:
        exclude_texts = []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    texts = set()

    for elem in root.iter():
        if (elem.attrib.get('package') == package and
                elem.attrib.get('class') == class_name and
                elem.attrib.get('index') == index and
                elem.attrib.get('text') != "" and
                elem.attrib.get('resource-id') != 'com.mcu.reolink:id/device_name_tv' and
                elem.attrib.get('enabled') == "true"):

            text = elem.attrib.get('text')

            if text and text not in exclude_texts:
                texts.add(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        for text in sorted(texts):
            f.write(text + '\n')

    with open(output_path, 'r', encoding='utf-8') as f:
        non_empty_lines = sum(1 for line in f if line.strip())

    print(f"总非空行数: {non_empty_lines}")


xml_path = 'D:\\app-uiauto-test-dev\\debug\\destination4.xml'
output_path = 'D:\\app-uiauto-test-dev\\elements_texts.txt'
package = "com.mcu.reolink"
class_name = "android.widget.TextView"
index = "0"
exclude_texts = ["开", "关", "设置", "报警设置", "报警通知", "更多", "0", "退出登录设备", "删除"]

parse_and_extract_text(xml_path, output_path, package, class_name, index, exclude_texts)
