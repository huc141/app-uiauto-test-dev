def verify_wifi_battery_page():
    logger.info('开始执行wifi设备-电池模块的验证')

    def check_and_click_agree():
        self.click_by_text(text='同意并继续')
        time.sleep(2)
        RemoteSetting().scroll_check_funcs2(texts=options, scroll_or_not=False, back2top=False)

    def check_and_click_close_statistics():
        self.click_by_xpath(xpath_expression=self.battery_data_off_button)
        time.sleep(1)
        self.click_by_text(text='关闭统计')

    def confirm_close_statistics():
        RemoteSetting().scroll_check_funcs2(texts=battery_off_button, scroll_or_not=False, back2top=False)
        self.click_by_text(text='取消')
        check_and_click_close_statistics()
        self.click_by_text(text='确定')
        time.sleep(2)
        RemoteSetting().scroll_check_funcs2(texts=text, scroll_or_not=False, back2top=False)

    if self.loop_detect_element_exist(element_value='同意并继续'):
        RemoteSetting().scroll_check_funcs2(texts=text, scroll_or_not=False, back2top=False)
        check_and_click_agree()
    elif self.loop_detect_element_exist(element_value='最近4周运行时长'):
        RemoteSetting().scroll_check_funcs2(texts=options, scroll_or_not=False, back2top=False)
        confirm_close_statistics()
    else:
        logger.info('未检测到“同意并继续”和“最近4周运行时长”文案，可能是4G设备，执行4G设备的验证')
