import time
from time import sleep

import pydirectinput
import keyboard
import threading

from get_container_item_relative_coord import GetContainerItemRelativeCoord
from windowed_coord import WindowedCoord



class Module2:
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        print(f"Module1 初始化，参数: {param1}")

        # 全局变量存储线程对象
        self.thread = None

        # 标志位
        self.running = False

        # 设置 pydirectinput 的延迟（关键优化）
        pydirectinput.PAUSE = 0.01  # 加在这里，确保所有操作生效
        pydirectinput.FAILSAFE = False  # 禁用安全检查

        print(pydirectinput.PAUSE)


    def execute(self):
        """根据参数执行不同的功能"""
        # if self.param1 == "清背包":
        #     self.function_a()
        self.function_a()

    def function_a(self):
        print("Module1 执行功能A")
        self.on_key_press()

    def on_key_press(self):
        print(f"执行on_key_press")
        if self.thread is None or not self.thread.is_alive():
            print("1")
            self.running = True
            self.thread = threading.Thread(target=self.on_thirteen_gun)
            # 标志位，用于关闭线程的循环
            self.thread.start()
        else:
            print("2")
            self.running = False  # 修改标志位
            self.thread.join()  # 等待线程结束

    def on_thirteen_gun(self):
        print("执行on_thirteen_gun")
        # SetClientAreaResolution("Path of Exile", 1068, 601)
        container_type = ""
        capacity = 0
        if self.param2 == "小仓":
            capacity = 144
            if self.param3 == "不嵌套":
                container_type = "small_warehouse_no_nesting"
            elif self.param3 == "嵌套":
                container_type = "small_warehouse_is_nesting"
        elif self.param2 == "大仓":
            capacity = 576
            if self.param3 == "不嵌套":
                container_type = "large_warehouse_no_nesting"
            elif self.param3 == "嵌套":
                container_type = "large_warehouse_is_nesting"
        backpack = GetContainerItemRelativeCoord(container_type , 1)

        i = 0
        while self.running and i < capacity:
            # 清包
            x, y = backpack.get_coord(i)
            pydirectinput.moveTo(x, y)
            pydirectinput.keyDown("ctrl")
            pydirectinput.mouseDown(button='left')
            pydirectinput.mouseUp(button='left')
            i += 1
        pydirectinput.keyUp("ctrl")
