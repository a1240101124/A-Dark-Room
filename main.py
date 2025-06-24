# ///////////////////////////////////////////////////////////////
#
# 作者: WANDERSON M.PIMENTA
# 使用工具: Qt Designer 和 PySide6
# 版本: 1.0.0
#
# 本项目可自由使用于任何用途，但需在Python脚本中保留相应版权信息，
# 可视化界面(GUI)中的任何信息可随意修改，无需承担任何责任。
#
# 如果你想将产品用于商业用途，Qt许可证存在限制，建议阅读官方网站：
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import ctypes
import os
import sys

# 导入 / 图形界面、模块和控件
# ///////////////////////////////////////////////////////////////
from modules import *  # noqa: F403
from widgets import *  # noqa: F403

os.environ["QT_FONT_DPI"] = "96"  # 修复高DPI和缩放比例超过100%的显示问题

# 设置为全局控件
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):  # noqa: F405
    def __init__(self):
        QMainWindow.__init__(self)  # noqa: F405

        # 设置为全局控件
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()  # noqa: F405
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # 使用自定义标题栏 | 在Mac或Linux系统中使用"False"
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True  # noqa: F405

        # 应用名称
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - 现代图形界面"    # 任务栏名称
        description = "PyDracula应用 - 基于Dracula主题的Python界面。" # 标题
        # 应用文本设置
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # 初始化界面拖拽移动属性
        self.mouse_pressed = False
        self.offset = None

        # 切换菜单
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))  # noqa: F405

        # 设置界面定义
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)  # noqa: F405

        # QTableWidget参数设置
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # noqa: F405

        # 按钮点击事件
        # ///////////////////////////////////////////////////////////////

        # 左侧菜单
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # 左侧扩展栏
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)  # noqa: F405

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # 右侧扩展栏
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)  # noqa: F405

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # 显示应用
        # ///////////////////////////////////////////////////////////////
        self.show()

        # 设置自定义主题，False：暗黑主题，True：亮主题
        # 设置为True，再打包成exe后，可能会出现路径问题，即找不到主题位置
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = True
        themeFile = r"themes\py_dracula_light.qss"

        # 设置主题和修复
        if useCustomTheme:
            # 加载并应用样式
            UIFunctions.theme(self, themeFile, True)  # noqa: F405

            # 设置修复
            AppFunctions.setThemeHack(self)  # noqa: F405

        # 设置主页并选择菜单
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))  # noqa: F405

    # 按钮点击事件
    # 在这里添加按钮点击后的功能函数
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # 获取被点击的按钮
        btn = self.sender() # QObject 类的自带方法，获取发出信号的对象
        btnName = btn.objectName()

        # 显示主页
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)  # noqa: F405
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # noqa: F405

        # 显示控件页面
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)  # noqa: F405
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # noqa: F405

        # 显示新页面
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # 设置页面
            UIFunctions.resetStyle(self, btnName)  # 重置其他按钮的选中状态  # noqa: F405
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # 选中当前菜单  # noqa: F405

        if btnName == "btn_save":
            print("保存按钮被点击!")

        # 打印按钮名称
        print(f'按钮 "{btnName}" 被按下!')

    # 调整大小事件
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # 更新大小控制手柄
        UIFunctions.resize_grips(self)  # noqa: F405

    # 鼠标点击事件
    # ///////////////////////////////////////////////////////////////
    # def mousePressEvent(self, event):
    #     # 设置窗口拖动位置
    #     self.dragPos = event.globalPos()

    #     # 打印鼠标事件
    #     if event.buttons() == Qt.LeftButton:  # noqa: F405
    #         print("鼠标点击: 左键点击")
    #     if event.buttons() == Qt.RightButton:  # noqa: F405
    #         print("鼠标点击: 右键点击")

    # 鼠标拖拽标题栏移动UI界面
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # 使用实际的标题栏组件名称：contentTopBg
        if event.button() == Qt.LeftButton and widgets.contentTopBg.geometry().contains(event.position().toPoint()):  # noqa: F405
            self.mouse_pressed = True
            self.offset = event.globalPosition().toPoint() - self.pos()
        super().mousePressEvent(event)  # 调用父类方法，确保其他功能正常

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and self.offset is not None:
            self.move(event.globalPosition().toPoint() - self.offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # noqa: F405
            self.mouse_pressed = False
            self.offset = None
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("by.阿斗是只猫.专利标注辅助.v1.0")  # 唯一标识

    ICON_PATH = "icon.ico"

    app = QApplication(sys.argv)  # noqa: F405
    app.setWindowIcon(QIcon(ICON_PATH))  # noqa: F405
    window = MainWindow()
    sys.exit(app.exec())
