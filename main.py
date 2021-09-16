import sys
import time
from functools import partial
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import QThread, Signal,QCoreApplication,QRect,QSize
from functools import partial
import base64
from close_png import img as close_  
from open_png import img as open_
#图片解码
close_pic = open('figure/close.png', 'wb')        
close_pic.write(base64.b64decode(close_))    
close_pic.close() 

open_pic = open('figure/open.png', 'wb')        
open_pic.write(base64.b64decode(open_))    
open_pic.close()

class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.b_up = []
        self.b_down = []
        self.b_key = []
        self.l_elevators = []
        self.l_floor = []
        self.l_up = []
        self.l_down = []
        self.b_warning = []
        self.setupUi()

    def pause(self,i):
        i -= 1
        if i in pause_list:
            pause_list.remove(i)
            self.b_warning[i].setStyleSheet("border: 1px solid #ccb3b3;border-radius:8; text-align:center;line-height:25px;color:rgb(255,255,255)")
        else:
            pause_list.append(i)
            self.b_warning[i].setStyleSheet("border: 1px solid #ccb3b3;border-radius:8; text-align:center;line-height:25px;color:rgb(255,0,0)")

    def want_open(self,i): 
        pix = QPixmap("figure/open.png")
        self.l_elevators[i -1].setPixmap(pix)
        self.l_elevators[i -1].setScaledContents(True)
        should_pause[i -1] = 1
    
    def want_close(self,i):
        pix = QPixmap("figure/close.png")
        self.l_elevators[i -1].setPixmap(pix)
        self.l_elevators[i -1].setScaledContents(True)

    def set_goal(self,i, j):  #设定目标楼层
        if i not in pause_list:
            self.b_key[i][j].setStyleSheet(u"border: 1px solid rgba(83, 166, 249, 255);border-radius:8;text-align: center;line-height: 25px;color:rgb(255,128,64)")
            
            elevator_goal[i].add(j + 1)
   
    #优先级调度算法 
    def priority_schedule(self,j):
        index = 0
        value = -2
        level = [0,0,0,0,0]
        for i in range(5):
            if state[i]:
                if state[i]*(j - floor[i]) < 0:
                    level[i] = -1
                else:
                    level[i] = 20 - state[i]*(j - floor[i])
            else:
                level[i] = 20 - abs(j - floor[i])
        for i in range(5):
            if level[i] > value and i not in pause_list:
                value = level[i]
                index = i
        return index
    
    def set__goal_up(self,j):  #设定楼道里上楼请求所在的楼层
        for i in range(5):
            if i not in pause_list:
                self.b_up[i][j].setStyleSheet("background-color:rgb(255,255,255)")
        j+=1
        index = self.priority_schedule(j)  
        elevator_goal[index].add(j)
        
    def set__goal_down(self,j):  # 设定楼道里下楼请求所在的楼层
        for i in range(5):
            if i not in pause_list:
                self.b_down[i][j].setStyleSheet("background-color:rgb(255,255,255)")
        j+=1
        index = self.priority_schedule(j)
        elevator_goal[index].add(j)

    def setupUi(self):
        global is_first
        self.resize(905, 641)
        for i in range(1,6):
            b_u = []
            b_d = []
            b_k = []
            b_d.append(0)
            self.b_up.append(b_u)
            self.b_down.append(b_d)
            self.b_key.append(b_k)
            self.elevator = QFrame(self)
            self.elevator.setObjectName(u"elevator"+str(i))
            self.elevator.setGeometry(QRect(10+180*(i-1), 0, 159, 531))
            self.elevator.setMaximumSize(QSize(16777215, 16777215))
            self.elevator.setStyleSheet(u"background-color:#BBDEFB;border-radius: 15px;height:90%;")
            self.elevator.setFrameShape(QFrame.StyledPanel)
            self.elevator.setFrameShadow(QFrame.Raised)
            #电梯外部控制
            self.out = QFrame(self.elevator)
            self.out.setObjectName(u"out_"+str(i))
            self.out.setGeometry(QRect(0, 0, 101, 411))
            self.out.setStyleSheet(u"background-color:rgba(83, 166, 249, 255); border-radius: 15px;background-color:#1976D2; height = 60%;")
            self.out.setFrameShape(QFrame.StyledPanel)
            self.out.setFrameShadow(QFrame.Raised)
            for j in range(1,21):
                #楼层标识
                self.label_num = QLabel(self.out)
                self.label_num.setObjectName(u"label_num_"+str(j)+"_"+str(i))
                self.label_num.setGeometry(QRect(10, 410-20*j, 21, 16))
                self.label_num.setAutoFillBackground(False)
                self.label_num.setStyleSheet(u"color:rgb(255,255,255)")
                self.label_num.setFrameShape(QFrame.NoFrame)
                if j<10:
                    self.label_num.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">L0"+str(j)+"</span></p></body></html>", None))
                else:
                    self.label_num.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">L"+str(j)+"</span></p></body></html>", None))
                #向上/下按钮  
                if(j!=1):
                    self.button_down = QPushButton(self.out)
                    self.button_down.setObjectName("button_down{0}+{1}".format(j,i))
                    self.button_down.setGeometry(QRect(80, 410-20*j, 16, 16))
                    self.button_down.setText(QCoreApplication.translate("MainWindow", u"\u25bc", None))
                    self.button_down.clicked.connect(partial(self.set__goal_down,j-1))
                    b_d.append(self.button_down)
                        
                if(j!=20):
                    self.button_up = QPushButton(self.out)
                    self.button_up.setObjectName("button_up{0}+{1}".format(j,i))
                    self.button_up.setGeometry(QRect(60, 410-20*j, 16, 16))
                    self.button_up.setText(QCoreApplication.translate("MainWindow", u"\u25b2", None))
                    self.button_up.clicked.connect(partial(self.set__goal_up,j-1))
                    b_u.append(self.button_up)      
                       
            pix = QPixmap("close.png")
            self.lb = QLabel(self.elevator)
            self.lb.setPixmap(pix)
            self.lb.setGeometry(QRect(115,390,20,20))
            self.lb.setScaledContents(True)
            self.l_elevators.append(self.lb)
            
            #电梯内部控制
            self.in_ = QFrame(self.elevator)
            self.in_.setObjectName(u"in_"+str(i))
            self.in_.setGeometry(QRect(0, 410, 159, 121))
            self.in_.setStyleSheet(u"border-radius:15px;background-color:#42A5F5;height:30%;")
            self.in_.setFrameShape(QFrame.StyledPanel)
            self.in_.setFrameShadow(QFrame.Raised)
            #警报按钮
            self.warning = QPushButton(self.in_)
            self.warning.setObjectName(u"warning"+str(i))
            self.warning.setGeometry(QRect(70, 0, 21, 21))
            self.warning.setMinimumSize(QSize(0, 0))
            self.warning.setStyleSheet(u"border: 1px solid #ccb3b3;border-radius:8;color: rgb(255,255,255); text-align: center;line-height: 25px;")
            self.warning.setText(QCoreApplication.translate("MainWindow", u"!", None))
            self.warning.clicked.connect(partial(self.pause,i))
            self.b_warning.append(self.warning)
            #开门按钮
            self.open = QPushButton(self.in_)
            self.open.setObjectName(u"open_"+str(i))
            self.open.setGeometry(QRect(100, 0, 21, 21))
            self.open.setMinimumSize(QSize(0, 0))
            self.open.setStyleSheet(u"border: 1px solid #ccb3b3;border-radius:8; color:rgb(255,255,255);text-align: center;line-height: 25px;")
            self.open.setText(QCoreApplication.translate("MainWindow", u"<>", None))
            self.open.clicked.connect(partial(self.want_open,i))
            #关门按钮
            self.close = QPushButton(self.in_)
            self.close.setObjectName(u"close_"+str(i))
            self.close.setGeometry(QRect(130, 0, 21, 21))
            self.close.setMinimumSize(QSize(0, 0))
            self.close.setStyleSheet(u"border: 1px solid #ccb3b3;border-radius:8;color:rgb(255,255,255);text-align: center;line-height: 25px;")
            self.close.setText(QCoreApplication.translate("MainWindow", u"><", None))
            self.close.clicked.connect(partial(self.want_close,i))
            #显示电梯移动方向
            self.label_up = QLabel(self.in_)
            self.label_up.setObjectName(u"label_up_"+str(i))
            self.label_up.setGeometry(QRect(10, 0, 16, 16))
            self.label_up.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:7pt;\">\u25b2</span></p></body></html>", None))
            self.l_up.append(self.label_up)
            self.label_down = QLabel(self.in_)
            self.label_down.setObjectName(u"label_down_"+str(i))
            self.label_down.setGeometry(QRect(10, 10, 16, 16))
            self.label_down.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:7pt;\">\u25bc</span></p></body></html>", None))
            self.l_down.append(self.label_down)
            #显示电梯所在楼层
            self.label_floor = QLabel(self.in_)
            self.label_floor.setObjectName(u"label_floor_"+str(i))
            self.label_floor.setGeometry(QRect(30, 0, 21, 21))
            self.label_floor.setStyleSheet(u"color: rgb(255,255,255)")
            self.label_floor.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">01</span></p></body></html>", None))
            self.l_floor.append(self.label_floor)
            #目标楼层按钮
            self.floor_button = QFrame(self.in_)
            self.floor_button.setObjectName(u"floor_button_"+str(i))
            self.floor_button.setGeometry(QRect(10, 20, 141, 91))
            self.floor_button.setStyleSheet(u"border-radius:15px; background-color: #E1F5FE;")
            self.floor_button.setFrameShape(QFrame.StyledPanel)
            self.floor_button.setFrameShadow(QFrame.Raised)
            for j in range(1,21):   
                self.key = QPushButton(self.floor_button)
                self.key.setObjectName("key{0}+{1}".format(j,i))
                self.key.setGeometry(QRect(30*((j-1)%5), 70-20*((j-1)//5), 21, 16))
                self.key.setStyleSheet(u"border: 1px solid rgba(83, 166, 249, 255);border-radius:8;text-align: center;line-height: 25px;")
                if j<10:
                    self.key.setText(QCoreApplication.translate("MainWindow", u"0"+str(j), None))
                else:
                    self.key.setText(QCoreApplication.translate("MainWindow", u""+str(j), None))
                self.key.clicked.connect(partial(self.set_goal,i-1,j-1))
                b_k.append(self.key)
        self.show()

        # setupUi

def update(i):
    if i not in pause_list:
      #移动电梯
        if state[i] == 0:
            pass
        elif state[i] == -1:
            floor[i] -= 1
        else:
            floor[i] += 1      
        ui.l_elevators[i].setGeometry(QRect(115,410-20*floor[i],20,20))

        #电梯内部显示楼层
        if floor[i] <10:
            ui.l_floor[i].setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">0"+str(floor[i])+"</span></p></body></html>", None))
        else:
            ui.l_floor[i].setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">"+str(floor[i])+"</span></p></body></html>", None))
        if floor[i] == 20:
            print(1)
        #电梯内部显示移动方向
        if state[i] == 1:
            ui.l_up[i].setStyleSheet("color:rgb(255,255,255)")
        elif state[i] == -1:
            ui.l_down[i].setStyleSheet("color:rgb(255,255,255)")
        else:
            ui.l_up[i].setStyleSheet("color:rgb(0,0,0)")
            ui.l_down[i].setStyleSheet("color:rgb(0,0,0)")
        
        #判断电梯是否到达
        if floor[i] in elevator_goal[i]:
            should_pause[i] = 1
            #移除标识
            ui.b_key[i][floor[i]-1].setStyleSheet(u"border: 1px solid rgba(83, 166, 249, 255);border-radius:8;text-align: center;line-height: 25px;")
            for k in range(5):
                if floor[i] < 20:
                    ui.b_up[k][floor[i]-1].setStyleSheet("")  
                ui.b_down[k][floor[i]-1].setStyleSheet("") 

        if floor[i]>20:
            floor[i] = 20
        elevator_goal[i].discard(floor[i])  # 从要达到的目标楼层中移除该层

#Look内部调度算法
def look_schedule(the_int):
    i = the_int -1
    if i not in pause_list:
       # update(i)
       
        #移动电梯
        if state[i] == 0:
            pass
        elif state[i] == -1:
            floor[i] -= 1
        else:
            floor[i] += 1      
        ui.l_elevators[i].setGeometry(QRect(115,410-20*floor[i],20,20))

        #电梯内部显示楼层
        if floor[i] <10:
            ui.l_floor[i].setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">0"+str(floor[i])+"</span></p></body></html>", None))
        else:
            ui.l_floor[i].setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">"+str(floor[i])+"</span></p></body></html>", None))
        if floor[i] == 20:
            print(1)
        #电梯内部显示移动方向
        if state[i] == 1:
            ui.l_up[i].setStyleSheet("color:rgb(255,255,255)")
        elif state[i] == -1:
            ui.l_down[i].setStyleSheet("color:rgb(255,255,255)")
        else:
            ui.l_up[i].setStyleSheet("color:rgb(0,0,0)")
            ui.l_down[i].setStyleSheet("color:rgb(0,0,0)")
        
        #判断电梯是否到达
        if floor[i] in elevator_goal[i]:
            should_pause[i] = 1
            #移除标识
            ui.b_key[i][floor[i]-1].setStyleSheet(u"border: 1px solid rgba(83, 166, 249, 255);border-radius:8;text-align: center;line-height: 25px;")
            for k in range(5):
                if floor[i] < 20:
                    ui.b_up[k][floor[i]-1].setStyleSheet("")  
                if floor[i] > 1:
                    ui.b_down[k][floor[i]-1].setStyleSheet("") 

        if floor[i]>20:
            floor[i] = 20
        elevator_goal[i].discard(floor[i])  # 从要达到的目标楼层中移除该层
        
        # ----------------------内部调度算法---------------------- #

        if state[i] == -1:  # 如果当前状态是向下
            if len(list(elevator_goal[i])) == 0:
                state[i] = 0
            if (len(list(elevator_goal[i])) != 0) and (min(list(elevator_goal[i])) > floor[i]):
                state[i] = 1

        if state[i] == 1:  # 如果当前状态是向上
            if len(list(elevator_goal[i])) == 0:
                state[i] = 0
            if (len(list(elevator_goal[i])) != 0) and (max(list(elevator_goal[i])) < floor[i]):
                state[i] = -1

        if state[i] == 0:  # 如果当前状态是静止
            if (len(list(elevator_goal[i])) != 0) and (max(list(elevator_goal[i])) > floor[i]):
                state[i] = 1
            if (len(list(elevator_goal[i])) != 0) and (min(list(elevator_goal[i])) < floor[i]):
                state[i] = -1

class WorkThread(QThread):
    # 实例化一个信号对象
    trigger = Signal(int)

    def __init__(self,the_int,ui):
        super(WorkThread, self).__init__()
        self.int = the_int
        self.trigger.connect(look_schedule)
        self.ui = ui

    def run(self):
        while (1):
            if should_pause[self.int -1] == 0:
                pix = QPixmap("close.png")
                self.ui.l_elevators[self.int -1].setPixmap(pix)
                self.ui.l_elevators[self.int -1].setScaledContents(True)
            if should_pause[self.int -1] == 1:
                should_pause[self.int -1] = 0
                pix = QPixmap("open.png")
                self.ui.l_elevators[self.int -1].setPixmap(pix)
                self.ui.l_elevators[self.int -1].setScaledContents(True)
                time.sleep(1)
                
            self.trigger.emit(self.int)
            time.sleep(1)

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = Ui()
     # 表示目标楼层
    temp1 = set([])
    temp2 = set([])
    temp3 = set([])
    temp4 = set([])
    temp5 = set([])

    elevator_goal = [temp1,temp2,temp3,temp4,temp5]

    should_pause = [0, 0, 0, 0, 0]

    # 此数组表示电梯状态 0表示停止 1表示向上运行 -1表示向下运行
    state = [0,0,0,0,0]

    # 表示当前楼层
    floor = [1,1,1,1,1]

    pause_list = []

    # 表示楼道里的向上的请求
    people_up = set([])

    # 表示楼道里的向下的请求
    people_down = set([])
    # 五个线程对应五部电梯，每隔一定时间检查每部电梯的状态和elevator_goal数组，并作出相应的行动
    t1 = WorkThread(1,ui)
    t2 = WorkThread(2,ui)
    t3 = WorkThread(3,ui)
    t4 = WorkThread(4,ui)
    t5 = WorkThread(5,ui)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    sys.exit(app.exec_())

