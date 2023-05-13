import collections
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class settings_window(QDialog):
    def __init__(self, parent=None):
        super(settings_window, self).__init__(parent)

        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        # layout = QVBoxLayout()
        layout = QGridLayout()
        # 创建一个标签和一个文本框，并将它们添加到布局中
        label1 = QLabel("棋盘长宽:", self)
        self.textbox1 = QLineEdit(self)
        self.textbox1.setText('19')
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.textbox1, 0, 1)

        # 创建另一个标签和文本框，并将它们添加到布局中
        label2 = QLabel("灰色棋子数量:", self)
        self.textbox2 = QLineEdit(self)
        self.textbox2.setText('0')
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.textbox2, 1, 1)

        # 创建另一个标签和文本框，并将它们添加到布局中
        label3 = QLabel("红色棋子数量:", self)
        self.textbox3 = QLineEdit(self)
        self.textbox3.setText('0')
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.textbox3, 2, 1)

        label4 = QLabel("局时(分钟):", self)
        self.textbox4 = QLineEdit(self)
        self.textbox4.setText('30')
        layout.addWidget(label4, 3, 0)
        layout.addWidget(self.textbox4, 3, 1)

        label5 = QLabel("读秒(秒):", self)
        self.textbox5 = QLineEdit(self)
        self.textbox5.setText('60')
        layout.addWidget(label5, 4, 0)
        layout.addWidget(self.textbox5, 4, 1)

        label6 = QLabel("获胜条件,黑子比白子多多少目:", self)
        self.textbox6 = QLineEdit(self)
        self.textbox6.setText('7.5')
        layout.addWidget(label6, 5, 0)
        layout.addWidget(self.textbox6, 5, 1)

        # 创建一个确认按钮
        self.button = QPushButton('确认', self)
        layout.addWidget(self.button, 6, 0, 1, 2)

        self.label = QLabel(self)
        self.label.setText(
            "灰色棋子为不可被吃,不可移动的障碍物\n红色棋子为不可被吃障碍物,每步随机向一个可以移动的方向移动一步\n 本系统没有判断打劫的功能,请自行遵守棋规")
        layout.addWidget(self.label, 7, 0, 1, 2)
        # 设置窗口的布局
        self.setLayout(layout)

        # 创建一个正则表达式来限制文本框中只能输入数字
        regex = QRegExp("[0-9.]*")
        validator = QRegExpValidator(regex)

        # 将正则表达式验证器设置为文本框的验证器
        self.textbox1.setValidator(validator)
        self.textbox2.setValidator(validator)
        self.textbox3.setValidator(validator)
        self.textbox4.setValidator(validator)
        self.textbox5.setValidator(validator)
        self.textbox6.setValidator(validator)

        # 连接按钮的clicked信号到槽函数onButtonClicked
        self.button.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        # 当确认按钮被单击时，检查文本框中的文本是否为空
        if not self.textbox1.text() or not self.textbox2.text() or not self.textbox3.text() or not self.textbox4.text() or not self.textbox5.text() or not self.textbox6.text():
            # 如果文本框为空，则弹出一个错误提示框
            QMessageBox.critical(self, "错误", "文本框不能为空！")
        else:
            # 否则，获取文本框中的文本并更新内部变量
            self.n = self.textbox1.text()
            self.grey = self.textbox2.text()
            self.red = self.textbox3.text()
            self.time = self.textbox4.text()
            self.eachtime = self.textbox5.text()
            self.wincondition = self.textbox6.text()
            if int(self.n) <= 1:
                QMessageBox.critical(self, "错误", "长宽过小！")
            elif int(self.time) == 0:
                QMessageBox.critical(self, "错误", "局时不能为0！")
            else:
                self.parent().handle_arg(
                    f'{self.n} {self.red} {self.grey} {self.time} {self.eachtime} {self.wincondition}')
                self.accept()
                self.close()
