name：（必需）配置项名称
desc：（必需）配置项的描述，通常包括其功能和用途，以及入口路径
type：（必需）配置项的类型，说明其在界面的表现形式
    page：表示一个页面
    navigation：导航菜单，点击可以进入下一级页面
    switch：开关类型，点击开启或关闭
    popup：弹出菜单，点击显示选项列表
    text：纯文本显示，点击无反应
    checkbox: 多选按钮，点击选中或取消选中
    slider: 滑块，滑动横条
items：（可选）当配置项类型为 `page` 时使用，列出子配置项
options：（可选）当配置项为`popup`或`checkbox`时使用，列出用户可以选择的选项
subpage：（可选）当配置项类型为 `navigation` 时使用，定义子级页面

```yaml
main_page:
  name: '主页面'
desc: '这是主页面，包含多个菜单项'
type: 'page'
items:
  popup_type_menu_name:
    name: '菜单名称1'
    desc: '点击后出现弹窗的菜单'
    type: 'popup'
    options:
      - '选项a'
      - '选项b'
  checkbox_type_menu_name:
    name: '菜单名称2'
    desc: '点击后出现弹窗的菜单'
    type: 'checkbox'
    options:
      - '选项a'
      - '选项b'
  switch_type_menu_name:
    name: '菜单名称3'
    desc: '点击后切换开关状态的菜单'
    type: 'switch'
  text_type_menu_name:
    name: '菜单名称4'
    desc: '点击后无反应，仅显示文本信息的菜单'
    type: 'text'
  nav_type_menu_name:
    name: '菜单名称5'
    desc: '点击后跳转到子页面的菜单'
    type: 'navigation'
    subpage:
      name: '子页面'
      desc: '子级页面的说明'
      type: 'page'

```