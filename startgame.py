import collections
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from TDWidgets import *
import settings


class BaseBoard(QWidget):
    '''
    游戏对战窗体的基类
    '''

    def __init__(self, n=19, red=0, grey=0):
        super().__init__()
        self.n = n
        self.red = red
        self.grey = grey
        self.initUI()

    def initUI(self):
        # 初始化ui
        self.wide = 1100
        self.high = 900
        self.timeju = 30
        self.timebu = 60
        self.wincondition = 7.5
        self.is_over = False
        self.zhong = False
        self.gridhistory=collections.deque()
        self.history = collections.deque()
        self.setGeometry(100, 100, self.wide, self.high)
        self.setWindowTitle('围棋游戏')
        self.grid = [[0] * (self.n + 2) for _ in range(self.n + 2)]
        self.player = 1
        self.initboard()
        self.randomgreyblock(self.grey)
        self.randomredblock(self.red)
        self.drawtaiji()
        self.drawtime()

        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('source/游戏界面.jpg')))  # 设置背景图片
        self.setPalette(palette1)

        self.back_button = TDPushButton(self, 'source/过一手_normal.png', 'source/过一手_hover.png',
                                        'source/过一手_press.png', parent=self)
        self.back_button.click_signal.connect(self.playerpass)
        self.back_button.move(915, 480)

        self.setting_button = TDPushButton(self, 'source/设置_normal.png', 'source/设置_hover.png',
                                           'source/设置_press.png', parent=self)
        self.setting_button.click_signal.connect(self.show_settings)
        self.setting_button.move(915, 660)

        self.restart_button = TDPushButton(self, 'source/开始_normal.png', 'source/开始_hover.png',
                                           'source/开始_press.png', parent=self)
        self.restart_button.click_signal.connect(self.restart)
        self.restart_button.move(915, 420)

        self.huiqi_button = TDPushButton(self, 'source/悔棋_normal.png', 'source/悔棋_hover.png',
                                         'source/悔棋_press.png', parent=self)
        self.huiqi_button.click_signal.connect(self.undo)
        self.huiqi_button.move(915, 540)

        self.renshu_button = TDPushButton(self, 'source/认输_normal.png', 'source/认输_hover.png',
                                          'source/认输_press.png', parent=self)
        self.renshu_button.click_signal.connect(self.win)
        self.renshu_button.move(915, 600)

        self.shumu_button = TDPushButton(self, 'source/数目_normal.png', 'source/数目_hover.png',
                                         'source/数目_press.png', parent=self)
        self.shumu_button.click_signal.connect(self.deadcheck)
        self.shumu_button.move(915, 720)

    def deadcheck(self):
        if self.is_over==True:
            return
        self.player2_timer.stop()
        self.player1_timer.stop()
        if self.zhong == False:
            self.history.clear()
            self.gridhistory.clear()
            QMessageBox.information(self, '提子', "请单击棋盘把死棋提取,随后再次点击数目按钮")
            self.zhong = True
        else:
            vst = set()
            dx = [0, 0, 1, -1]
            dy = [1, -1, 0, 0]
            black, white = 0, 0
            for i in range(1, self.n + 1):
                for j in range(1, self.n + 1):

                    if self.grid[i][j] == 1: black += 1
                    if self.grid[i][j] == 2: white += 1
                    k=len(vst)
                    if (i, j) not in vst and self.grid[i][j] == 0:
                        vst.add((i, j))
                        color = set()
                        que = collections.deque()
                        que.append((i, j))
                        while que:
                            x, y = que.popleft()
                            vst.add((x, y))
                            for d in range(4):
                                a = x + dx[d]
                                b = y + dy[d]
                                if self.grid[a][b] == 0:
                                    if (a, b) not in vst:
                                        vst.add((a, b))
                                        que.append((a, b))
                                else:
                                    color.add(self.grid[a][b])
                        if 1 in color and 2 in color:
                            black += (len(vst)-k) / 2
                            white += (len(vst)-k) / 2
                        elif 1 in color and 2 not in color:
                            black += (len(vst)-k)
                        elif 2 in color and 1 not in color:
                            white += (len(vst)-k)
            if black - white >= self.wincondition:
                self.player = 2
                self.win()
                QMessageBox.information(self, '黑子获胜',
                                        f"黑子{black}目, 白子{white}目.\n双方的差值为{abs(- black + white)}目,黑子需要多白子{self.wincondition}目能获胜")
            else:
                self.player = 1
                self.win()

                QMessageBox.information(self, '白子获胜',
                                        f"黑子{black}目, 白子{white}目.\n双方的差值为{abs(- black + white)}目,黑子需要多白子{self.wincondition}目才能获胜")

    def restart(self):
        self.initboard()
        self.randomredblock(self.red)
        self.randomgreyblock(self.grey)
        self.player = 1
        self.zhong = False
        self.history.clear()
        self.gridhistory.clear()
        if self.is_over == True:
            self.win_label.close()
            self.is_over = False
            self.win_label = None
        self.taiji_label.close()
        self.drawtaiji()
        self.player1_timer.stop()
        self.player2_timer.stop()
        self.player1_time = QTime(0, self.timeju, 0)
        self.player2_time = QTime(0, self.timeju, 0)
        self.player1_time_label.setText(self.player1_time.toString('mm:ss'))
        self.player2_time_label.setText(self.player2_time.toString('mm:ss'))

        self.update()

    def handle_arg(self, text):
        self.n, self.red, self.grey, self.timeju, self.timebu, self.wincondition = map(float, text.split())
        self.n, self.red, self.grey, self.timeju, self.timebu = int(self.n), int(self.red), int(self.grey), int(
            self.timeju), int(self.timebu)
        self.n=min(self.n,50)
        self.timeju=min(self.timeju,59)
        self.timebu=min(self.timeju,59*60)
        self.restart()

    def show_settings(self):
        self.settings = settings.settings_window(self)
        self.settings.setWindowTitle("设置")
        self.settings.exec_()

    def initboard(self):
        '''初始化棋盘'''
        self.grid = [[0] * (self.n + 2) for i in range(self.n + 2)]
        for i in range(self.n + 2):
            self.grid[i][0] = 3
            self.grid[self.n + 1][i] = 3
            self.grid[i][self.n + 1] = 3
            self.grid[0][i] = 3

    def randomgreyblock(self, scale):
        '''设置随机障碍块'''
        tmp = scale
        tmp = min(tmp, self.n * self.n - self.grey)
        while tmp != 0:
            x = random.randint(1, self.n)
            y = random.randint(1, self.n)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 3
                tmp -= 1

    def randomredblock(self, scale):
        '''设置随机障碍块'''
        tmp = scale
        tmp = min(tmp, self.n * self.n)
        while tmp != 0:
            x = random.randint(1, self.n)
            y = random.randint(1, self.n)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 4
                tmp -= 1

    def paintEvent(self, event):
        '''画布'''
        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        self.drawPieces(qp)

        qp.end()

    def drawtime(self):
        self.player1_time = QTime(0, self.timeju, 0)
        self.player2_time = QTime(0, self.timeju, 0)

        self.player1_time_label = QLabel(self.player1_time.toString('mm:ss'), self)
        self.player1_time_label.move(915, 350)
        self.player1_time_label.setStyleSheet("QLabel{color:rgb(255,255,255,255);font-size:40px;font-weight:bold;}")

        self.player2_time_label = QLabel(self.player2_time.toString('mm:ss'), self)
        self.player2_time_label.move(915, 300)
        self.player2_time_label.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:40px;font-weight:bold;}")

        self.player1_timer = QTimer(self)
        self.player1_timer.timeout.connect(self.player1_timeout)

        self.player2_timer = QTimer(self)
        self.player2_timer.timeout.connect(self.player2_timeout)
        self.current_player = 2

    def player1_timeout(self):
        self.player1_time = self.player1_time.addSecs(-1)
        self.player1_time_label.setText(self.player1_time.toString('mm:ss'))

        if self.player1_time == QTime(0, 0, 0):
            self.msg_box("白子超时")
            self.win()
            self.player1_timer.stop()

    def player2_timeout(self):
        self.player2_time = self.player2_time.addSecs(-1)
        self.player2_time_label.setText(self.player2_time.toString('mm:ss'))
        if self.player2_time == QTime(0, 0, 0):
            self.msg_box("黑子超时")
            self.win()
            self.player2_timer.stop()

    def switch_player(self):
        mm, ss = map(int, self.player1_time.toString('mm:ss').split(':'))
        if mm * 60 + ss < self.timebu:
            self.player1_time = QTime(0, self.timebu // 60, self.timebu % 60)
            self.player1_time_label.setText(self.player1_time.toString('mm:ss'))

        mm, ss = map(int, self.player2_time.toString('mm:ss').split(':'))
        if mm * 60 + ss < self.timebu:
            self.player2_time = QTime(0, self.timebu // 60, self.timebu % 60)
            self.player2_time_label.setText(self.player2_time.toString('mm:ss'))

        if self.player == 1:
            self.player1_timer.stop()
            self.player2_timer.start(1000)
        else:
            self.player2_timer.stop()

            self.player1_timer.start(1000)

    def start_timer(self):
        self.player1_timer.start(1000)
        self.current_player = 1

    def drawtaiji(self):
        if self.player == 1:
            taiji_pic = QPixmap('source/B.png')
            self.taiji_label = QLabel(parent=self)
            self.taiji_label.setPixmap(taiji_pic)
            self.taiji_label.resize(taiji_pic.size())
            self.taiji_label.move(878, 80)
            self.taiji_label.show()
        else:
            taiji_pic = QPixmap('source/W.png')
            self.taiji_label = QLabel(parent=self)
            self.taiji_label.setPixmap(taiji_pic)
            self.taiji_label.resize(taiji_pic.size())
            self.taiji_label.move(922, 80)
            self.taiji_label.show()

    def win(self):
        '''
        黑旗胜利或者白棋胜利了
        '''
        if self.is_over == True:
            return
        self.player1_timer.stop()
        self.player2_timer.stop()
        if self.player == 2:
            win_pic = QPixmap('source/黑棋胜利.png')
        else:
            win_pic = QPixmap('source/白棋胜利.png')
        self.win_label = QLabel(parent=self)
        self.win_label.setPixmap(win_pic)
        self.win_label.resize(win_pic.size())
        self.win_label.move(250, 250)  # 显示游戏结束的图片
        self.win_label.show()

        self.is_over = True

    def playerpass(self):
        if self.is_over == True:
            return
        self.player = 3 - self.player
        self.history.append((0, 0, set(), 3))
        self.gridhistory.append(''.join([''.join(map(str,self.grid[i])) for i in range(1,self.n+1)]))


        self.blockmove()
        self.taiji_label.close()
        self.drawtaiji()
        self.update()

    def drawGrid(self, qp):
        '''划线'''
        a = 800 // (self.n - 1)
        pen = QPen(Qt.black, 4, Qt.SolidLine)
        qp.setPen(pen)
        i = 0
        qp.drawLine(50, 50 + i * a, 50 + a * (self.n - 1), 50 + i * a)
        qp.drawLine(50 + i * a, 50, 50 + i * a, 50 + a * (self.n - 1))
        i = self.n - 1
        qp.drawLine(50, 50 + i * a, 50 + a * (self.n - 1), 50 + i * a)
        qp.drawLine(50 + i * a, 50, 50 + i * a, 50 + a * (self.n - 1))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(1,self.n-1):
            qp.drawLine(50, 50 + i * a, 50 + a * (self.n - 1), 50 + i * a)
            qp.drawLine(50 + i * a, 50, 50 + i * a, 50 + a * (self.n - 1))



    def blockmove(self):
        # 移动阻隔块
        dx = [0, 0, -1, 1]
        dy = [1, -1, 0, 0]

        nowpos = []
        nextpos = []
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if self.grid[i][j] == 4:
                    nowpos.append((i, j))

        for x, y in nowpos:
            choicemove = [(x, y)]
            for d in range(4):
                a = x + dx[d]
                b = y + dy[d]
                if self.grid[a][b] == 0:
                    choicemove.append((a, b))
            t = random.choice(choicemove)
            while t in nextpos:
                t = random.choice(choicemove)
            nextpos.append(t)

        for i in range(len(nextpos)):
            a, b = nowpos[i]
            self.grid[a][b] = 0
            a, b = nextpos[i]
            self.grid[a][b] = 4
        for a, b in nextpos:
            t = set()
            t |= self.Check(1, a, b - 1, 2)
            t |= self.Check(1, a - 1, b, 2)
            t |= self.Check(1, a, b + 1, 2)
            t |= self.Check(1, a + 1, b, 2)
            t |= self.Check(2, a, b - 1, 2)
            t |= self.Check(2, a - 1, b, 2)
            t |= self.Check(2, a, b + 1, 2)
            t |= self.Check(2, a + 1, b, 2)
            for x, y in t: self.grid[x][y] = 0

    def drawPieces(self, qp):
        '''分块'''
        a = 800 // (self.n - 1)
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if self.grid[i][j] == 1:
                    brush = QBrush(Qt.black, Qt.SolidPattern)
                    qp.setBrush(brush)
                    qp.drawEllipse(50 + (i - 1) * a - a // 3, 50 + (j - 1) * a - a // 3, 2 * a // 3, 2 * a // 3)
                elif self.grid[i][j] == 2:
                    brush = QBrush(Qt.white, Qt.SolidPattern)
                    qp.setBrush(brush)
                    qp.drawEllipse(50 + (i - 1) * a - a // 3, 50 + (j - 1) * a - a // 3, 2 * a // 3, 2 * a // 3)
                elif self.grid[i][j] == 3:
                    brush = QBrush(Qt.gray, Qt.SolidPattern)
                    qp.setBrush(brush)
                    qp.drawEllipse(50 + (i - 1) * a - a // 3, 50 + (j - 1) * a - a // 3, 2 * a // 3, 2 * a // 3)

                elif self.grid[i][j] == 4:
                    brush = QBrush(Qt.red, Qt.SolidPattern)
                    qp.setBrush(brush)
                    qp.drawEllipse(50 + (i - 1) * a - a // 3, 50 + (j - 1) * a - a // 3, 2 * a // 3, 2 * a // 3)

    def mousePressEvent(self, event):
        '''鼠标点击事件'''
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()

            if x < 50 or y < 50 or x > 850 or y > 850 or self.is_over == True:
                return
            a = 800 // (self.n - 1)
            i = round((x - 50) / a) + 1
            j = round((y - 50) / a) + 1

            if self.zhong == True:
                if self.grid[i][j] == 0: return
                self.history.append((i, j, set(), self.grid[i][j]))

                self.grid[i][j] = 0
            else:
                if self.grid[i][j] != 0: return
                t = set()
                t |= self.Check(3 - self.player, i, j - 1, 1)
                t |= self.Check(3 - self.player, i - 1, j, 1)
                t |= self.Check(3 - self.player, i, j + 1, 1)
                t |= self.Check(3 - self.player, i + 1, j, 1)
                for x, y in t: self.grid[x][y] = 0
                if not t and not self.Check(self.player, i, j, 0): return
                self.history.append((i, j, t, 3 - self.player))

                state=''.join([''.join(map(str, self.grid[i])) for i in range(1, self.n + 1)])
                if state in self.gridhistory and t:
                    self.player=3-self.player
                    self.undo()
                    self.msg_box('打劫!')
                    self.gridhistory.append(state)
                    return

                self.gridhistory.append(state)

                self.grid[i][j] = self.player
                self.player = 3 - self.player
                self.blockmove()
                self.taiji_label.close()
                self.drawtaiji()
                self.switch_player()
            self.update()

    def msg_box(self, msg):
        QMessageBox.critical(self, "错误", msg)

    def Check(self, col, posx, posy, state):
        # 判断是否有气
        if self.grid[posx][posy] != col and state in [1, 2]:
            return set()
        dx = [0, 0, -1, 1]
        dy = [1, -1, 0, 0]
        que = collections.deque()
        que.append((posx, posy))
        connect = set()
        connect.add((posx, posy))
        air = 0
        vst = set()
        while que:
            x, y = que.popleft()
            vst.add((x, y))

            for d in range(4):
                a = x + dx[d]
                b = y + dy[d]
                if (a, b) not in vst:
                    if self.grid[a][b] == 0:
                        air += 1
                    elif self.grid[a][b] == col:
                        que.append((a, b))
                        connect.add((a, b))
                    vst.add((a, b))
        # state为0,表示能否落子
        # state为1,表示能否提子
        if state == 0:
            if air == 0:
                self.msg_box("不能在此处落子")
                return False
            return True
        elif state == 1:
            if air == 1:
                return connect
            return set()
        elif state == 2:
            if air == 0:
                return connect
            return set()

    def undo(self):
        '''撤回功能'''
        if not self.history: return
        if self.zhong == True:
            x, y, t, p = self.history.pop()
            self.grid[x][y] = p
            self.update()
        else:
            if self.red != 0:
                self.msg_box("红色棋子存在时,不能悔棋!")
                return
            if self.red == 0 and self.is_over == False:
                self.player = 3 - self.player
                x, y, t, p = self.history.pop()
                self.gridhistory.pop()
                for a, b in t:
                    self.grid[a][b] = p
                self.grid[x][y] = 0
                self.taiji_label.close()
                self.drawtaiji()
                self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = BaseBoard()
    main.show()
    sys.exit(app.exec_())
