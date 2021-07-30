import sys
import os
import numpy as np
import cv2
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading


main_ui = uic.loadUiType('sw_window.ui')[0]
fourcc = cv2.VideoWriter_fourcc(*'DIVX')


class MyApp(QMainWindow, main_ui):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.initUI()

        # 변수 초기화
        self.init_dir = './'
        self.video_path = []

        self.cam_num =0
        self.cap = None
        self.press_esc = False
        self.video_frame = False


        # 버튼에 기능 연결
        self.cam_comboBox.currentIndexChanged.connect(self.camSetting_combo) # 캠 번호
        self.cam_pushButton.clicked.connect(self.camSetting_button) # 캠 선택 버튼
        self.cam_message = QMessageBox() # 캠 메시지
        self.video_pushButton.clicked.connect(self.getVideo_button) # 비디오 선택 버튼
        self.video_listWidget.itemDoubleClicked.connect(self.selectVideo) # 비디오 리스트 중 선택
        self.videoplay_pushButton.clicked.connect(self.Video_button)

        self.exit_Button.clicked.connect(self.prgram_exit) # 종료 버튼

    def initUI(self):
        self.setWindowTitle('1-stage detection')
        # self.setWindowIcon()
        self.cam_comboBox.addItem('0')
        self.cam_comboBox.addItem('1')
        self.cam_comboBox.addItem('2')
        self.cam_comboBox.addItem('3')
        self.center()
        self.show()

    def camSetting_combo(self):
        self.cam_num = int(self.cam_comboBox.currentText())

    def camSetting_button(self):
        self.cap = cv2.VideoCapture(self.cam_num, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            self.cam_message.setWindowTitle('Message')
            self.cam_message.setIcon(QMessageBox.Information)
            self.cam_message.setText('This cam is not work')
            self.cam_message.setStandardButtons(QMessageBox.Ok)
            retval = self.cam_message.exec_()

            self.cap = None
        else:
            self.startCamera()

    def startCamera(self):
        if self.cap:
            while True:
                self.ret, self.frame = self.cap.read()

                if self.ret:
                    self.showImage(self.frame, self.display_label)
                    cv2.waitKey(1)
                else:
                    break
        print('1')
        self.cap.release()

    def getVideo_button(self):
        self.video_path = QFileDialog.getOpenFileNames(self, 'Select video', self.init_dir)[0]
        print(self.video_path)
        # self.video_label.setText(video_path)

        if self.video_path:
            for i, path in enumerate(self.video_path):
                self.video_listWidget.insertItem(i, os.path.basename(path))
        else:
            self.video_listWidget.clear()


    def selectVideo(self):
        self.idx = self.video_listWidget.currentRow()
        self.cap = cv2.VideoCapture(self.video_path[self.idx])

        self.ret, self.frame = self.cap.read()
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if self.ret:
            self.video_frame = True
            self.showImage(self.frame, self.display_label)

    def Video_button(self):
        if self.video_frame:
            self.video_frame = False
            print(self.video_frame)
            self.startVideo()
        else:
            self.video_frame = True
            print(self.video_frame)


    def startVideo(self):
        print(self.video_frame)
        if self.cap:
            while True:
                self.ret, self.frame = self.cap.read()

                if self.ret and not self.video_frame:
                    self.showImage(self.frame, self.display_label)
                    cv2.waitKey(1)
                elif self.ret:
                    break


    def showImage(self, img, display_label):
        draw_img = img.copy()
        height = display_label.height()
        width = display_label.width()
        bytesPerLine = 3 * width

        draw_img = cv2.resize(draw_img, (height, width))

        qt_image = QImage(draw_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        qpixmap = QPixmap.fromImage(qt_image)
        display_label.setPixmap(qpixmap)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def prgram_exit(self):
        self.press_esc = True
        QCoreApplication.instance().quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_window = MyApp()
    my_window.show()
    sys.exit(app.exec_())
