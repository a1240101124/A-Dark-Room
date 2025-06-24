# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
from pathlib import Path

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *  # noqa: F403

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class UIFunctions(MainWindow):  # type: ignore # noqa: F405
    # MAXIMIZE/RESTORE 最大化 / 还原
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status is False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(":/icons/images/icons/icon_restore.png"))  # type: ignore # noqa: F405
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(":/icons/images/icons/icon_maximize.png"))  # type: ignore # noqa: F405
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS 返回状态
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return GLOBAL_STATE

    # SET STATUS 设置状态
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU 切换菜单
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH 获取宽度
            width = self.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH  # type: ignore # noqa: F405
            standard = 60

            # SET MAX WIDTH 设置最大宽度
            if width == 60:  # noqa: SIM108
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION 动画
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")  # type: ignore # noqa: F405
            self.animation.setDuration(Settings.TIME_ANIMATION)  # type: ignore # noqa: F405
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)  # type: ignore # noqa: F405
            self.animation.start()

    # TOGGLE LEFT BOX 切换左侧框
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH 获取宽度
            width = self.ui.extraLeftBox.width()
            widthRightBox = self.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH  # type: ignore # noqa: F405
            color = Settings.BTN_LEFT_BOX_COLOR  # type: ignore # noqa: F405
            standard = 0

            # GET BTN STYLE 获取按钮样式
            style = self.ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH 设置最大宽度
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ""))  # type: ignore # noqa: F405
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ""))

        UIFunctions.start_box_animation(self, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX 切换右侧框
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH 获取宽度
            width = self.ui.extraRightBox.width()
            widthLeftBox = self.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH  # type: ignore # noqa: F405
            color = Settings.BTN_RIGHT_BOX_COLOR  # type: ignore # noqa: F405
            standard = 0

            # GET BTN STYLE 获取按钮样式
            style = self.ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH 设置最大宽度
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN 选择按钮
                self.ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.ui.toggleLeftBox.styleSheet()
                    self.ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ""))  # type: ignore # noqa: F405
            else:
                widthExtended = standard
                # RESET BTN 复位按钮
                self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ""))

            UIFunctions.start_box_animation(self, widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0

        # Check values 检查数值
        if left_box_width == 0 and direction == "left":  # noqa: SIM108
            left_width = 240
        else:
            left_width = 0
        # Check values 检查数值
        if right_box_width == 0 and direction == "right":  # noqa: SIM108
            right_width = 240
        else:
            right_width = 0

        # ANIMATION LEFT BOX 动画左框
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")  # type: ignore # noqa: F405
        self.left_box.setDuration(Settings.TIME_ANIMATION)  # type: ignore # noqa: F405
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)  # type: ignore # noqa: F405

        # ANIMATION RIGHT BOX 动画右框
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")  # type: ignore # noqa: F405
        self.right_box.setDuration(Settings.TIME_ANIMATION)  # type: ignore # noqa: F405
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)  # type: ignore # noqa: F405

        # GROUP ANIMATION  群组动画
        self.group = QParallelAnimationGroup()  # type: ignore # noqa: F405
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    # SELECT/DESELECT MENU 选择 / 取消选择菜单
    # ///////////////////////////////////////////////////////////////
    # SELECT 选择
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET  # type: ignore # noqa: F405
        return select

    # DESELECT 取消
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")  # type: ignore # noqa: F405
        return deselect

    # START SELECTION 开始选择
    def selectStandardMenu(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):  # type: ignore # noqa: F405
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    # RESET SELECTION 重置选择
    def resetStyle(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):  # type: ignore # noqa: F405
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS 导入主题文件 QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            # str = open(file).read()
            # self.ui.styleSheet.setStyleSheet(str)
            path = Path(file)
            try:
                # 读取 QSS 内容并应用样式
                self.ui.styleSheet.setStyleSheet(path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"加载主题失败：{e}，请检查文件路径是否正确")

    # START - GUI DEFINITIONS 开始 导入主题文件 QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:  # type: ignore # noqa: F405
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))  # type: ignore # noqa: F405

        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:  # type: ignore # noqa: F405
            # STANDARD TITLE BAR 开始 - 图形用户界面定义
            self.setWindowFlags(Qt.FramelessWindowHint)  # type: ignore # noqa: F405
            self.setAttribute(Qt.WA_TranslucentBackground)  # type: ignore # noqa: F405

            # MOVE WINDOW / MAXIMIZE / RESTORE 移动窗口 / 最大化 / 恢复
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL 如果最大化，则更改为正常
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW 移动窗口
                if event.buttons() == Qt.LeftButton:  # type: ignore # noqa: F405
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS 定制握把
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)  # type: ignore # noqa: F405
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)  # type: ignore # noqa: F405
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)  # type: ignore # noqa: F405
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)  # type: ignore # noqa: F405

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW 投影
        self.shadow = QGraphicsDropShadowEffect(self)  # type: ignore # noqa: F405
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))  # type: ignore # noqa: F405
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW 调整窗口大小
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)  # type: ignore # noqa: F405
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE 最小化
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE 最大化 / 恢复
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION 关闭应用程序
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:  # type: ignore # noqa: F405
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS 结束 - 图形用户界面定义
