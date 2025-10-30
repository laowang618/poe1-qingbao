import pydirectinput
import threading

from get_container_item_relative_coord import GetContainerItemRelativeCoord



class Module1:
    def __init__(self, param1,param2):
        self.param1 = param1
        self.param2 = param2
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
        backpack = GetContainerItemRelativeCoord("backpack", 1)
        i = 0
        while self.running and i < 60:
            print(i)
            # 清包
            x, y = backpack.get_coord(i)
            pydirectinput.moveTo(x, y)
            pydirectinput.keyDown("ctrl")
            if self.param2 == "不分类":
                pydirectinput.keyDown("shift")
            pydirectinput.mouseDown(button='left')
            pydirectinput.mouseUp(button='left')
            i += 1
        pydirectinput.keyUp("ctrl")
        if self.param2 == "不分类":
            pydirectinput.keyUp("shift")
