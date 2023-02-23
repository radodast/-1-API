import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic



class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('apelsin.ui', self)
        self.l = 'skl'
        self.cords = ['55.755864', '37.617698']
        self.size = ['1', '1']
        self.map_file = "map.png"
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.getImage()
        self.setWindowTitle('Отображение карты')
        self.mapB.clicked.connect(self.refl)
        self.sat.clicked.connect(self.refl)
        self.skl.clicked.connect(self.refl)



    def refl(self):
        l = self.sender().text()
        if l == 'схема':
            self.l = 'skl'
            self.getImage()
        if l == 'спутник':
            self.l = 'sat'
            self.getImage()
        if l == 'гибрид':
            self.l = 'map'
            self.getImage()

        ## Изображение

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(self.cords)}&spn={','.join(self.size)}&l={self.l}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.map.setPixmap(QPixmap(self.map_file))

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.size[0] != '64.0':
                self.size = [str(float(self.size[0]) * 2), str(float(self.size[0]) * 2)]
                self.getImage()
        if event.key() == Qt.Key_PageUp:
            if self.size[0] != '0.0078125':
                self.size = [str(float(self.size[0]) / 2), str(float(self.size[0]) / 2)]
                self.getImage()
        if event.key() == Qt.Key_Up:
            self.cords[1] = str(float(self.cords[1]) + 1.0)
            self.getImage()
        if event.key() == Qt.Key_Down:
            self.cords[1] = str(float(self.cords[1]) - 1.0)
            self.getImage()
        if event.key() == Qt.Key_Right:
            self.cords[0] = str(float(self.cords[0]) + 1.0)
            self.getImage()
        if event.key() == Qt.Key_Left:
            self.cords[0] = str(float(self.cords[0]) - 1.0)
            self.getImage()



def exept_hook(cls, exeption, traceback):
    sys.__excepthook__(cls, exeption, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = exept_hook
    sys.exit(app.exec_())
