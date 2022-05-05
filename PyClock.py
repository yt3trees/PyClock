from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        # jsonファイルの読み込み
        jsonPath = "./config.json"
        jsonValues = self.load_json(jsonPath)
        self.gifPath = jsonValues.get('gifPath')

        super(Ui_MainMenu, self).__init__()
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(1920, 515)
        MainMenu.setWindowTitle("PyClock")
        # 画面サイズを取得
        desktop = QtWidgets.QDesktopWidget()
        geometry = desktop.screenGeometry()
        # ウインドウサイズ(枠込)を取得
        framesize = MainMenu.frameSize()
        # ウインドウの位置を指定
        MainMenu.move(geometry.width() / 2 - framesize.width() / 2, geometry.height() / 2 - framesize.height() / 2)

        # self.window = QtWidgets.QWidget()

        self.centralwidget = self.set_gif(self.gifPath)
        self.centralwidget.setObjectName("centralwidget")
        MainMenu.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainMenu)
        # self.statusbar.setObjectName("statusbar")
        # MainMenu.setStatusBar(self.statusbar)
        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

        layout = QtWidgets.QGridLayout()

        # 時計ラベル
        self.label = QtWidgets.QLabel(MainMenu)
        self.label.setFixedWidth(450)
        self.label.setFixedHeight(200)
        # font = QtGui.QFont()
        # font.setPointSize(150)
        # font.setFamily("MS UI Gothic")
        # self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(#"QLabel{background:white;}"
                   "QLabel{color:White;font-size:150px;font-weight:bold;font-family:ＭＳ 明朝 ;}"
                   "QLabel{border-style:outset;border-width:10px;border-color:White;}"
                   )
        self.label.move(200, 130)
        # 日付ラベル
        self.labelDate = QtWidgets.QLabel(MainMenu)
        self.labelDate.setAlignment(QtCore.Qt.AlignLeft)
        self.labelDate.setFixedWidth(450)
        self.labelDate.setStyleSheet(#"QLabel{background:white;}"
                   "QLabel{color:White;font-size:30px;font-weight:bold;font-family:ＭＳ 明朝 ;}"
                   )
        self.labelDate.move(340, 340)

        self.timer = QtCore.QTimer(MainMenu)
        # self.update_time()

        self.timer.timeout.connect(self.update_time)
        self.timer.start()

        # ショートカット
        # Escキーを押したら終了
        self.shortcutEsc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), MainMenu)
        self.shortcutEsc.activated.connect(MainMenu.close)
        # self.labelDateをクリックしたら終了
        self.label.mousePressEvent = lambda event: self.save_json(MainMenu, jsonPath)
        MainMenu.mousePressEvent = lambda event: MainMenu.close()

        # layout.addWidget(self.label,0,0,1,2)
        # MainMenu.setLayout(layout)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "PyClock"))

    def set_gif(self, gif_path):
        '''背景のgifファイルをセットする'''
        movie = QtGui.QMovie()
        movie.setFileName(gif_path)
        movie_label = QtWidgets.QLabel()
        movie_label.setMovie(movie)
        movie.start()
        return movie_label

    def update_time(self):
        '''時刻更新'''
        locale = QtCore.QLocale("en_US")
        # 時計を表示
        time = QtCore.QDateTime.currentDateTime()
        second = locale.toString(time, "ss")
        # second  = time.toString("ss")
        if int(second) % 2 == 0:
            timedisplay = time.toString("hh:mm") # yyyy-MM-dd hh:mm:ss
        else:
            timedisplay = time.toString("hh mm")
        self.label.setText(timedisplay)
        # 日付と曜日を表示
        datedisplay = locale.toString(time, "ddd, MMM dd")
        self.labelDate.setText(datedisplay)

    def file_select(self, Mainmenu):
        '''ファイル選択'''
        fileName = QtWidgets.QFileDialog.getOpenFileName(Mainmenu, 'Open file', './images/', "GIF files (*.gif)")
        print('selected file:', 'None' if fileName[0] == '' else fileName[0])
        return fileName[0]

    def load_json(self, jsonPath):
        '''jsonファイル読み込み'''
        try:
            if os.path.exists(jsonPath):
                jsonOpen = open(jsonPath,"r")
                jsonLoad = json.load(jsonOpen)
                return jsonLoad
        except Exception as e:
            e = "jsonファイルの読み込みに失敗しました。\n" + str(e)
            print(e)
            QtWidgets.QMessageBox.critical(None, "Error", e, QtWidgets.QMessageBox.Yes)

    def save_json(self, Mainmenu, jsonPath):
        '''
        jsonファイルに保存
        '''
        self.gifPath = self.file_select(Mainmenu)
        # .gifファイル以外を選択した場合は終了
        if os.path.splitext(self.gifPath)[1] != '.gif' and self.gifPath != "":
            QtWidgets.QMessageBox.critical(None, "Error", '.gifファイルのみを選択してください', QtWidgets.QMessageBox.Yes)
            return
        if self.gifPath != "":
            list = {
                "gifPath" : self.gifPath
            }
            try:
                if os.path.exists(jsonPath):
                    with open(jsonPath, 'w') as f:
                        json.dump(list, f, indent=1, ensure_ascii=False)
                    QtWidgets.QMessageBox.information(None, "info", "gifファイルを選択しました。\n次回起動時に反映されます。", QtWidgets.QMessageBox.Yes)
            except Exception as e:
                e = "jsonファイルの書き込みに失敗しました。\n" + str(e)
                print(e)
                QtWidgets.QMessageBox.critical(None, "Error", e, QtWidgets.QMessageBox.Yes)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainMenu = QtWidgets.QMainWindow()
    MainMenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)#| # ウインドウの枠を消す
                            # QtCore.Qt.WindowStaysOnTopHint) # ウインドウを常に最前面に表示
    ui = Ui_MainMenu()
    ui.setupUi(MainMenu)
    MainMenu.show()
    sys.exit(app.exec_())