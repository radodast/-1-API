import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cords = ['55.755864', '37.617698']
        self.size = ['1', '1']
        self.map_file = "map.png"
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.getImage()
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение



    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(self.cords)}&spn={','.join(self.size)}&l=map"
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

def exept_hook(cls, exeption, traceback):
    sys.__excepthook__(cls, exeption, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = exept_hook
    sys.exit(app.exec_())