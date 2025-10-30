import win32gui
import pydirectinput


class WindowedCoord:
    """
    窗口坐标转换装饰器类

    用于将1920x1080全屏坐标转换为"Path of Exile"游戏窗口内的实际屏幕坐标
    主要处理窗口边框、标题栏以及窗口缩放带来的坐标偏移问题
    """

    def __init__(self, func):
        """
        初始化装饰器

        Args:
            func: 被装饰的函数
        """
        print("初始化WindowedCoord")

        # 存储被装饰的函数引用
        self.func = func

        # 窗口句柄，用于标识特定的窗口实例
        self.hwnd = None

        # 窗口矩形坐标 (left, top, right, bottom)
        # 包含窗口边框和标题栏的完整窗口区域
        self.window_rect = None

        # 客户区矩形坐标 (left, top, right, bottom)
        # 不包含边框和标题栏，仅游戏画面显示区域
        self.client_rect = None

        # 客户区实际宽度和高度（像素）
        self.client_w = 0
        self.client_h = 0

        # 客户区左上角在屏幕坐标系中的绝对位置
        self.client_left = 0
        self.client_top = 0

        # X轴和Y轴的缩放比例
        # 用于将1920x1080坐标缩放到实际窗口大小
        self.scale_x = 1.0
        self.scale_y = 1.0

        # 查找游戏窗口并初始化窗口信息
        self._find_window_and_update()

    def _find_window_and_update(self):
        """
        查找"Path of Exile"游戏窗口并更新窗口信息

        Raises:
            RuntimeError: 当未找到指定窗口时抛出异常
        """
        # 通过窗口标题查找游戏窗口句柄
        hwnd = win32gui.FindWindow(None, "Path of Exile")
        if hwnd == 0:
            raise RuntimeError("未找到窗口 'Path of Exile'")
        self.hwnd = hwnd

        # 更新窗口的几何信息
        self._update_window_info()

    def _update_window_info(self):
        """
        更新窗口的几何信息和缩放比例

        获取当前窗口的位置、大小以及客户区信息，
        并重新计算坐标转换所需的缩放比例
        """
        # 获取窗口矩形：包含完整窗口（边框+标题栏+客户区）
        self.window_rect = win32gui.GetWindowRect(self.hwnd)  # (left, top, right, bottom)

        # 获取客户区矩形：仅游戏画面区域（不包含边框和标题栏）
        self.client_rect = win32gui.GetClientRect(self.hwnd)  # (left, top, right, bottom)

        # 计算客户区实际尺寸（像素）
        self.client_w = self.client_rect[2] - self.client_rect[0]  # right - left
        self.client_h = self.client_rect[3] - self.client_rect[1]  # bottom - top

        # 将客户区左上角的相对坐标转换为屏幕绝对坐标
        # 这样可以得到游戏画面在屏幕上的实际位置
        self.client_left, self.client_top = win32gui.ClientToScreen(self.hwnd,
                                                                    (self.client_rect[0], self.client_rect[1]))

        # 计算相对于1920x1080标准分辨率的缩放比例
        # 用于将标准坐标转换为实际窗口大小下的坐标
        self.scale_x = self.client_w / 1920
        self.scale_y = self.client_h / 1080

    def __call__(self, instance, x, y):
        """
        装饰器调用方法

        将1920x1080全屏坐标转换为实际窗口内的屏幕坐标，
        然后调用被装饰的函数

        Args:
            instance: 类实例（如果是实例方法的话）
            x: 标准1920x1080分辨率下的X坐标
            y: 标准1920x1080分辨率下的Y坐标

        Returns:
            被装饰函数的返回值
        """
        # 每次调用前更新窗口信息，确保坐标转换准确性
        # 即使窗口被移动或调整大小也能正确转换坐标
        self._update_window_info()

        # 将标准坐标按比例缩放到实际客户区大小
        x_window = x * self.scale_x
        y_window = y * self.scale_y

        # 将窗口内相对坐标转换为屏幕绝对坐标并取整
        # ClientToScreen已提供客户区左上角绝对坐标，直接相加即可
        x_abs = int(round(self.client_left + x_window))
        y_abs = int(round(self.client_top + y_window))

        # 调用原始函数，传入转换后的绝对屏幕坐标
        return self.func(instance, x_abs, y_abs)

    def refresh(self):
        """
        手动刷新窗口信息

        当需要强制更新窗口位置和大小信息时调用此方法
        """
        self._update_window_info()


# 使用示例
if __name__ == "__main__":
    @WindowedCoord
    def aaa(instance, x, y):
        """
        测试函数：移动鼠标到指定坐标

        Args:
            instance: 类实例（此处为None）
            x: 屏幕绝对X坐标
            y: 屏幕绝对Y坐标
        """
        pydirectinput.moveTo(x, y)


    # 测试点击中心位置 (1920x1080分辨率的中心点)
    aaa(None, 1296, 614)