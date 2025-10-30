import sys
import keyboard
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QComboBox, QStatusBar, QPushButton, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor, QBrush
import threading


class StatusIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.color = QColor(255, 0, 0)  # 初始红色

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(0, 0, 20, 20)


class GlobalKeyListener(QObject):
    f1_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.listening = False
        self.listener_thread = None

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.listener_thread = threading.Thread(target=self._listen_to_keyboard, daemon=True)
            self.listener_thread.start()

    def stop_listening(self):
        self.listening = False
        keyboard.unhook_all()  # 确保停止时取消所有hook
        if self.listener_thread:
            self.listener_thread.join(timeout=0.1)
            self.listener_thread = None

    # TODO 性能优化
    # def _listen_to_keyboard(self):
    #     keyboard.on_press_key('F1', lambda _: self.f1_pressed.emit())
    #     while self.listening:
    #         pass
    #     keyboard.unhook_all()
    def _listen_to_keyboard(self):
        # 先取消之前的hook
        keyboard.unhook_all()
        # 重新注册
        keyboard.on_press_key('F1', lambda _: self.f1_pressed.emit())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 二级联动下拉框(全局F1监听)")
        self.setGeometry(100, 100, 400, 200)

        self.current_module = None
        self.current_instance = None
        self.key_listener = GlobalKeyListener()
        self.key_listener.f1_pressed.connect(self.on_f1_pressed)

        self.init_ui()
        self.set_initial_state()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 第一级下拉框
        self.first_level_combo = QComboBox()
        self.first_level_combo.addItems(["选择模块", "入仓", "取仓"])
        self.first_level_combo.currentIndexChanged.connect(self.on_first_level_changed)

        # 第二级下拉框
        self.second_level_combo = QComboBox()
        self.second_level_combo.setEnabled(False)
        self.second_level_combo.currentIndexChanged.connect(self.on_second_level_changed)

        # TODO 三级下拉
        self.third_level_combo = QComboBox()
        self.third_level_combo.setEnabled(False)
        self.third_level_combo.currentIndexChanged.connect(self.on_third_level_changed)


        # 状态栏
        self.status_bar = QStatusBar()

        # 状态指示器
        self.status_indicator = StatusIndicator()

        # 运行/停止按钮
        self.run_button = QPushButton("运行")
        self.run_button.clicked.connect(self.on_run_clicked)

        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.on_stop_clicked)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.status_indicator)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()

        # 添加到主布局
        main_layout.addWidget(self.first_level_combo)
        main_layout.addWidget(self.second_level_combo)
        # TODO 三级下拉
        main_layout.addWidget(self.third_level_combo)
        main_layout.addLayout(button_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def set_initial_state(self):
        """设置初始状态"""
        self.status_indicator.set_color(QColor(255, 0, 0))  # 红色
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def set_state1(self):
        """状态1：选择好下拉框后"""
        self.status_indicator.set_color(QColor(255, 255, 0))  # 黄色
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def set_state2(self):
        """状态2：运行中"""
        self.status_indicator.set_color(QColor(0, 255, 0))  # 绿色
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def set_state3(self):
        """状态3：停止后"""
        if self.first_level_combo.currentIndex() > 0 and self.second_level_combo.currentIndex() >= 0:
            self.set_state1()
        else:
            self.set_initial_state()

    def on_first_level_changed(self, index):
        """第一级下拉框变化事件"""
        self.second_level_combo.clear()
        self.second_level_combo.setEnabled(False)

        # 获取第一级下拉的文本（而不是依赖 index）
        current_text = self.first_level_combo.currentText()

        if current_text == "选择模块":  # "选择模块"
            self.set_initial_state()
            return

        self.second_level_combo.setEnabled(True)

        # 根据第一级选择设置第二级选项
        if current_text == "入仓":  # 入仓
            self.second_level_combo.addItems(["清背包"])
            # self.current_module = "module1"
        elif current_text == "取仓":  # 取仓
            self.second_level_combo.addItems(["大仓", "小仓"])
            # self.current_module = "module2"

    # def on_second_level_changed(self, index):
    #     """第二级下拉框变化事件"""
    #     if index >= 0:
    #         self.set_state1()
    #     else:
    #         self.set_initial_state()

    # TODO 三级下拉
    def on_second_level_changed(self, index):
        self.third_level_combo.clear()
        self.third_level_combo.setEnabled(True)

        # 获取第一级下拉的文本（而不是依赖 index）
        current_text = self.first_level_combo.currentText()

        # 根据第二级选择设置第三级选项
        if current_text == "入仓":  # 模块1
            self.third_level_combo.addItems(["分类", "不分类"])
            self.current_module = "module1"
        elif current_text == "取仓":  # 模块2
            self.third_level_combo.addItems(["嵌套", "不嵌套"])
            self.current_module = "module2"


    def on_third_level_changed(self, index):

        """第三级下拉框变化事件"""
        if index >= 0:
            self.set_state1()
        else:
            self.set_initial_state()

    def on_run_clicked(self):
        """运行按钮点击事件"""
        if self.first_level_combo.currentIndex() == 0 or self.second_level_combo.currentIndex() < 0:
            return

        self.set_state2()

        # 动态导入模块并创建实例
        if self.current_module == "module1":
            from module1 import Module1
            selected_param1 = self.second_level_combo.currentText()
            selected_param2 = self.third_level_combo.currentText()
            self.current_instance = Module1(selected_param1, selected_param2)
        elif self.current_module == "module2":
            from module2 import Module2
            selected_param1 = self.first_level_combo.currentText()
            selected_param2 = self.second_level_combo.currentText()
            selected_param3 = self.third_level_combo.currentText()
            self.current_instance = Module2(selected_param1, selected_param2, selected_param3)

        # 开始全局监听F1键
        self.key_listener.start_listening()

    def on_stop_clicked(self):
        """停止按钮点击事件"""
        self.key_listener.stop_listening()

        # 销毁实例
        if self.current_instance:
            print("已销毁")
            self.current_instance = None

        self.set_state3()

    def on_f1_pressed(self):
        """F1键按下事件"""
        if self.current_instance:
            self.current_instance.execute()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())