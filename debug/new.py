import time

import wda

c = wda.Client('http://localhost:8100')

s = c.session()


# 使用类名定位元素

def get_all_texts():
    my_set = set()
    temp = set()

    # 将元素存储在列表中
    # def get_elements_texts():
    elements = c(className='XCUIElementTypeStaticText', index=0).find_elements()
    static_text_elements = {element.text for element in elements}
    # print(static_text_elements)

    for element in static_text_elements:
        x, y, w, h = element.bounds
        if x == 31 and element.label is not None:
            temp.update(element.text)
            print(element)
            print(element.text)
            print(temp)

        # return temp

    # 获取当前页面所有元素的文本内容
    # for _ in range(1):
    #     # 获取当前页面所有元素的文本内容
    #     new_texts = get_elements_texts()
    #     my_set.update(new_texts)
    #
    #     c.swipe_up()
    #     time.sleep(0.5)
    #
    #     # 检查滑动后页面是否有变化
    #     new_texts = get_elements_texts()
    #     if not new_texts - my_set:
    #         break  # 如果滑动后没有新内容，退出循环
    #
    #     # 添加新获取的文本内容
    #     my_set.update(new_texts)
    #
    # print(my_set)


get_all_texts()
