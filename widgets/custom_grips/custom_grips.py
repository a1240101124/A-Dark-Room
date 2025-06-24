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

from PySide6.QtCore import *  # noqa: F403
from PySide6.QtGui import *  # noqa: F403
from PySide6.QtWidgets import *  # noqa: F403


class CustomGrip(QWidget):  # noqa: F405
    def __init__(self, parent, position, disable_color=False):
        # SETUP UI 设置用户界面
        QWidget.__init__(self)  # noqa: F405
        self.parent = parent
        self.setParent(parent)
        self.wi = Widgets()

        # SHOW TOP GRIP 显视顶部栏
        if position == Qt.TopEdge:  # noqa: F405
            self.wi.top(self)
            self.setGeometry(0, 0, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS 获取
            top_left = QSizeGrip(self.wi.top_left)  # noqa: F405
            top_right = QSizeGrip(self.wi.top_right)  # noqa: F405

            # RESIZE TOP 调整顶部大小
            def resize_top(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() - delta.y())
                geo = self.parent.geometry()
                geo.setTop(geo.bottom() - height)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.top.mouseMoveEvent = resize_top

            # ENABLE COLOR 启用颜色
            if disable_color:
                self.wi.top_left.setStyleSheet("background: transparent")
                self.wi.top_right.setStyleSheet("background: transparent")
                self.wi.top.setStyleSheet("background: transparent")

        # SHOW BOTTOM GRIP 显视底部栏
        elif position == Qt.BottomEdge:  # noqa: F405
            self.wi.bottom(self)
            self.setGeometry(0, self.parent.height() - 10, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS
            self.bottom_left = QSizeGrip(self.wi.bottom_left)  # noqa: F405
            self.bottom_right = QSizeGrip(self.wi.bottom_right)  # noqa: F405

            # RESIZE BOTTOM 调整底部大小
            def resize_bottom(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() + delta.y())
                self.parent.resize(self.parent.width(), height)
                event.accept()

            self.wi.bottom.mouseMoveEvent = resize_bottom

            # ENABLE COLOR 启用颜色
            if disable_color:
                self.wi.bottom_left.setStyleSheet("background: transparent")
                self.wi.bottom_right.setStyleSheet("background: transparent")
                self.wi.bottom.setStyleSheet("background: transparent")

        # SHOW LEFT GRIP 显视左侧栏
        elif position == Qt.LeftEdge:  # noqa: F405
            self.wi.left(self)
            self.setGeometry(0, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            # RESIZE LEFT 向左调整大小
            def resize_left(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() - delta.x())
                geo = self.parent.geometry()
                geo.setLeft(geo.right() - width)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.leftgrip.mouseMoveEvent = resize_left

            # ENABLE COLOR 启用颜色
            if disable_color:
                self.wi.leftgrip.setStyleSheet("background: transparent")

        # RESIZE RIGHT 向右调整大小
        elif position == Qt.RightEdge:  # noqa: F405
            self.wi.right(self)
            self.setGeometry(self.parent.width() - 10, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_right(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() + delta.x())
                self.parent.resize(width, self.parent.height())
                event.accept()

            self.wi.rightgrip.mouseMoveEvent = resize_right

            # ENABLE COLOR 启用颜色
            if disable_color:
                self.wi.rightgrip.setStyleSheet("background: transparent")

    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def resizeEvent(self, event):
        if hasattr(self.wi, "container_top"):
            self.wi.container_top.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, "container_bottom"):
            self.wi.container_bottom.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, "leftgrip"):
            self.wi.leftgrip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, "rightgrip"):
            self.wi.rightgrip.setGeometry(0, 0, 10, self.height() - 20)


class Widgets:
    def top(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        self.container_top = QFrame(Form)  # noqa: F405
        self.container_top.setObjectName("container_top")
        self.container_top.setGeometry(QRect(0, 0, 500, 10))  # noqa: F405
        self.container_top.setMinimumSize(QSize(0, 10))  # noqa: F405
        self.container_top.setMaximumSize(QSize(16777215, 10))  # noqa: F405
        self.container_top.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.container_top.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.top_layout = QHBoxLayout(self.container_top)  # noqa: F405
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName("top_layout")
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_left = QFrame(self.container_top)  # noqa: F405
        self.top_left.setObjectName("top_left")
        self.top_left.setMinimumSize(QSize(10, 10))  # noqa: F405
        self.top_left.setMaximumSize(QSize(10, 10))  # noqa: F405
        self.top_left.setCursor(QCursor(Qt.SizeFDiagCursor))  # noqa: F405
        self.top_left.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.top_left.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.top_left.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.top_layout.addWidget(self.top_left)
        self.top = QFrame(self.container_top)  # noqa: F405
        self.top.setObjectName("top")
        self.top.setCursor(QCursor(Qt.SizeVerCursor))  # noqa: F405
        self.top.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.top.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.top.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.top_layout.addWidget(self.top)
        self.top_right = QFrame(self.container_top)  # noqa: F405
        self.top_right.setObjectName("top_right")
        self.top_right.setMinimumSize(QSize(10, 10))  # noqa: F405
        self.top_right.setMaximumSize(QSize(10, 10))  # noqa: F405
        self.top_right.setCursor(QCursor(Qt.SizeBDiagCursor))  # noqa: F405
        self.top_right.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.top_right.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.top_right.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.top_layout.addWidget(self.top_right)

    def bottom(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        self.container_bottom = QFrame(Form)  # noqa: F405
        self.container_bottom.setObjectName("container_bottom")
        self.container_bottom.setGeometry(QRect(0, 0, 500, 10))  # noqa: F405
        self.container_bottom.setMinimumSize(QSize(0, 10))  # noqa: F405
        self.container_bottom.setMaximumSize(QSize(16777215, 10))  # noqa: F405
        self.container_bottom.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.container_bottom.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.bottom_layout = QHBoxLayout(self.container_bottom)  # noqa: F405
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setObjectName("bottom_layout")
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_left = QFrame(self.container_bottom)  # noqa: F405
        self.bottom_left.setObjectName("bottom_left")
        self.bottom_left.setMinimumSize(QSize(10, 10))  # noqa: F405
        self.bottom_left.setMaximumSize(QSize(10, 10))  # noqa: F405
        self.bottom_left.setCursor(QCursor(Qt.SizeBDiagCursor))  # noqa: F405
        self.bottom_left.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.bottom_left.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.bottom_left.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.bottom_layout.addWidget(self.bottom_left)
        self.bottom = QFrame(self.container_bottom)  # noqa: F405
        self.bottom.setObjectName("bottom")
        self.bottom.setCursor(QCursor(Qt.SizeVerCursor))  # noqa: F405
        self.bottom.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.bottom.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.bottom.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.bottom_layout.addWidget(self.bottom)
        self.bottom_right = QFrame(self.container_bottom)  # noqa: F405
        self.bottom_right.setObjectName("bottom_right")
        self.bottom_right.setMinimumSize(QSize(10, 10))  # noqa: F405
        self.bottom_right.setMaximumSize(QSize(10, 10))  # noqa: F405
        self.bottom_right.setCursor(QCursor(Qt.SizeFDiagCursor))  # noqa: F405
        self.bottom_right.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.bottom_right.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.bottom_right.setFrameShadow(QFrame.Raised)  # noqa: F405
        self.bottom_layout.addWidget(self.bottom_right)

    def left(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        self.leftgrip = QFrame(Form)  # noqa: F405
        self.leftgrip.setObjectName("left")
        self.leftgrip.setGeometry(QRect(0, 10, 10, 480))  # noqa: F405
        self.leftgrip.setMinimumSize(QSize(10, 0))  # noqa: F405
        self.leftgrip.setCursor(QCursor(Qt.SizeHorCursor))  # noqa: F405
        self.leftgrip.setStyleSheet("background-color: rgb(255, 121, 198);")
        self.leftgrip.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.leftgrip.setFrameShadow(QFrame.Raised)  # noqa: F405

    def right(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(500, 500)
        self.rightgrip = QFrame(Form)  # noqa: F405
        self.rightgrip.setObjectName("right")
        self.rightgrip.setGeometry(QRect(0, 0, 10, 500))  # noqa: F405
        self.rightgrip.setMinimumSize(QSize(10, 0))  # noqa: F405
        self.rightgrip.setCursor(QCursor(Qt.SizeHorCursor))  # noqa: F405
        self.rightgrip.setStyleSheet("background-color: rgb(255, 0, 127);")
        self.rightgrip.setFrameShape(QFrame.NoFrame)  # noqa: F405
        self.rightgrip.setFrameShadow(QFrame.Raised)  # noqa: F405
