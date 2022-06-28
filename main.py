import numpy as np
import imutils
import easyocr
from PIL import Image
from matplotlib import pyplot as pl
from imutils import contours
import numpy as np
import cv2
import imutils
import pytesseract
import sys  # sys нужен для передачи argv в QApplication
import os
from PIL import Image

from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import design  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    a=0
    def __init__(self):


        super().__init__()
        self.setupUi(self)
        self.but1.clicked.connect(self.image)

        self.but1.setText("Ашу")
        self.but2.setText("номерин табу")
        self.but2.clicked.connect(self.naiti)
    def image(self):
        global a
        fileName = QFileDialog.getOpenFileName(self, "Open Image", "", "")
        if fileName:
            self.lab1.setText(fileName[0])
            img = Image.open(fileName[0])
            new_image = img.resize((500, 500))
            new_image.save(fileName[0])
        self.pixmap = QPixmap(fileName[0])
        self.lab1.setPixmap(self.pixmap)
        a=fileName[0]
    def naiti(self):
        global a




        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        image = cv2.imread(a)

        image = imutils.resize(image, width=500)

        '''cv2.imshow("Original Image", image)
        cv2.waitKey(0)'''

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        '''cv2.imshow("1 - Grayscale Conversion", gray)
        cv2.waitKey(0)'''

        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        '''cv2.imshow("2 - Bilateral Filter", gray)
        cv2.waitKey(0)'''

        edged = cv2.Canny(gray, 170, 200)
        '''cv2.imshow("3 - Canny Edges", edged)
        cv2.waitKey(0)'''

        cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        img1 = image.copy()
        cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)
        '''cv2.imshow("4- All Contours", img1)
        cv2.waitKey(0)'''

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        NumberPlateCnt = None  # we currently have no Number plate contour


        img2 = image.copy()
        cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)
        '''cv2.imshow("5- Top 30 Contours", img2)
        cv2.waitKey(0)'''

        count = 0
        idx = 7
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                NumberPlateCnt = approx
                x, y, w, h = cv2.boundingRect(c)
                new_img = gray[y:y + h, x:x + w]
                cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img)
                idx += 1

                break

        cv2.drawContours(image, [NumberPlateCnt], -1, (0, 255, 0), 3)
        '''cv2.imshow("Final Image With Number Plate Detected", image)
        cv2.waitKey(0)'''

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        file_name2='Cropped Images-Text/7.png'
        img5 = cv2.imread('Cropped Images-Text/7.png')
        img5 = cv2.resize(img5, None, fx=5, fy=5)  # Увеличение изображения в 9 раз
        gray = cv2.cvtColor(img5, cv2.COLOR_BGR2RGB)
        '''cv2.imshow("sasd", gray)'''
        self.pixmap = QPixmap(file_name2)
        self.lab1.setPixmap(self.pixmap)
        balance = pytesseract.image_to_string(gray)
        '''self.lab1.setText(balance)'''


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()  # то запускаем функцию main()


