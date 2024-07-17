import xml.etree.ElementTree as ET


def parse_and_extract_text(xml_path, output_path, exclude_texts=None):
    if exclude_texts is None:
        exclude_texts = []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    texts = set()

    for elem in root.iter():
        if (elem.attrib.get('type') == "XCUIElementTypeStaticText" and
                elem.attrib.get('index') == "0" and
                elem.attrib.get('label') != "" and
                elem.attrib.get('x') != "0" and
                elem.attrib.get('accessible') != 'false'):

            text = elem.attrib.get('label')

            if text and text not in exclude_texts:
                texts.add(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        for text in sorted(texts):
            f.write(text + '\n')

    with open(output_path, 'r', encoding='utf-8') as f:
        non_empty_lines = sum(1 for line in f if line.strip())

    print(f"总非空行数: {non_empty_lines}")


xml_path = 'H:\\app-uiauto-test-dev\\debug\\destination4.xml'
output_path = 'H:\\app-uiauto-test-dev\\elements_texts.txt'
exclude_texts = ["开", "关", "设置", "报警设置", "报警通知", "更多", "0", "退出登录设备", "删除", "FE-W2"]

parse_and_extract_text(xml_path, output_path, exclude_texts)
