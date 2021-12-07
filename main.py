import sys
import datetime
from PyQt6 import uic, QtCore, QtGui, QtWidgets
import json
import requests
from requests.exceptions import HTTPError


class MainWindow(QtWidgets.QMainWindow):
    ServerAdress = "http://localhost:5000"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messanger.ui', self)
        self.pushButton1.clicked.connect(self.pushButton1_clicked)

    def pushButton1_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        UserName = self.lineEdit1.text()
        MessageText = self.lineEdit2.text()
        TimeStamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{UserName}\", \"MessageText\": \"{MessageText}\", \"TimeStamp\": \"{TimeStamp}\"}}"
        print("Отправлено сообщение: " + msg)
        url = self.ServerAdress + "/api/Messanger"
        data = json.loads(msg)
        r = requests.post(url, json=data)

    def GetMessage(self, id):
        url = self.ServerAdress + "/api/Messanger/" + str(id)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            return None
        except Exception as err:
            return None
        else:
            text = response.text
            return text

    def timerEvent(self):
        msg = self.GetMessage(self.MessageID)
        while msg is not None:
            msg = json.loads(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext = f"{TimeStamp} : <{UserName}> : {MessageText}"
            print(msgtext)
            self.listWidget1.insertItem(self.MessageID, msgtext)
            self.MessageID += 1
            msg = self.GetMessage(self.MessageID)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timerEvent)
    timer.start(5000)

    sys.exit(app.exec())

