



class Settings:

    """
    自动化常用到的一些设置, 
    多数为时长和间隔
    """
    # 等待间隔, 供wait()函数调用
    wait_interval = 0.5
    # 等待时长, 供wait()函数调用
    wait_duration = 20
    # 查找间隔, 供find_element()函数调用
    find_interval = 0.33
    # 写入间隔, 供write()函数调用
    write_interval = 0.25
    # 滑动所用时间, 供swipe()函数调用, 单位为ms
    swipe_duration = 500
    # 隐藏元素操作次数, 供click()待函数使用
    drag_hidden_ele_times = 3
    # 点击间隔, 供click()等函数使用
    click_interval = 0.75