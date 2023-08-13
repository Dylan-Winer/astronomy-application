
# Counting stars in night sky program
# Authors: Dylan Winer and Jake Kasitz
# Dr. Kyle Shaw
# 13 July 2022

# Form implementation generated from reading ui file 'starGUI1.ui'
# Created by: PyQt5 UI code generator 5.9.2

# Import all packages
import io
from skimage import io as ios
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os
import cv2
from PIL import Image
import numpy as np
from skimage.feature import blob_log
import matplotlib.pyplot as plt

global astronomer
class Ui_MainWindow(object):

    # Create astronomer class with most of astrono
    def astronomer(self, name, coords, date, moon_side):

        def moon_phase(moon_side):
            original = cv2.imread(newname)
            # select ROI function
            roi = cv2.selectROI(original)
            # print rectangle points of selected roi
            print(roi)
            # Crop selected roi from raw image
            cropped = original[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

            grayImage = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  # convert to gray
            (thresh, black_white) = cv2.threshold(grayImage, 40, 255, cv2.THRESH_BINARY)  # convert to black and white
            blurred = cv2.GaussianBlur(black_white, (15, 15), 0)
            threshed = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

            white_pix = np.sum(threshed == 255)
            black_pix = np.sum(threshed == 0)

            total_pixels = white_pix + black_pix
            ratio = white_pix / total_pixels
            print("White", white_pix)
            print("Black", black_pix)

            moon_side = moon_side.lower()
            print("Ratio", ratio)
            phase1 = ""
            if ratio <= 0.03:
                phase1 = "New Moon"
            elif 0.03 < ratio <= 0.37 and moon_side == 'r':
                phase1 = "Waxing Crescent"
            elif 0.37 < ratio <= 0.41 and moon_side == 'r':
                phase1 = "First Quarter"
            elif 0.41 < ratio <= 0.74 and moon_side == 'r':
                phase1 = "Waxing Gibbons"
            elif ratio > 0.74:
                phase1 = "Full Moon - Beware of werewolves"
            elif 0.41 < ratio <= 0.74 and moon_side == 'l':
                phase1 = "Waning Gibbons"
            elif 0.37 < ratio <= 0.41 and moon_side == 'l':
                phase1 = "Last Quarter"
            elif 0.03 < ratio <= 0.37 and moon_side == 'l':
                phase1 = "Waning Crescent"

            phase_text = str(phase1)
            self.phase.setText(phase_text)


            # show cropped image
            cv2.imshow("circle", threshed)
            # hold window
            cv2.waitKey(0)

        def find_constellations(coords, date):
            global latit
            global longit
            latit = coords[0]
            longit = coords[1]
            print("Coords are:", coords)
            print("Season is:", date)
            date = date.lower()
            hemisphere = ""
            constellations = []

            if coords[0] >= 0:
                hemisphere = "northern"
            elif coords[0] < 0:
                hemisphere = "southern"
            else:
                print("Invalid coordinates")
            print("Hemisphere is", hemisphere)

            if hemisphere == "northern" and date == "winter":
                constellations = ["Orion", "Gemini", "Taurus", "Ursa Minor"]
            if hemisphere == "northern" and date == "spring":
                constellations = ["Leo", "Virgo", "Ursa Minor"]
            if hemisphere == "northern" and date == "summer":
                constellations = ["Scorpius", "Sagittarius", "Cygnus", "Ursa Minor"]
            if hemisphere == "northern" and date == "fall":
                constellations = ["Pegasus", "Pisces", "Ursa Minor"]

            if hemisphere == "southern" and date == "winter":
                constellations = ["Aquila", "Cygnus", "Hercules", "Lyra", "Ophiuchus", "Sagittarius", "Scorpius"]
            if hemisphere == "southern" and date == "spring":
                constellations = ["Andromeda", "Aquarius", "Capricornus", "Pegasus", "Pisces"]
            if hemisphere == "southern" and date == "summer":
                constellations = ["Canis Major", "Cetus", "Eridanus", "Gemini", "Orion", "Perseus", "Taurus"]
            if hemisphere == "southern" and date == "fall":
                constellations = ["Bootes", "Cancer", "Crater", "Hydra", "Leo", "Virgo"]

            global constellations_lower
            constellations_lower = []
            for name in constellations:
                name_new = name.lower()
                constellations_lower.append(name_new)

            print("Names of constellations:", constellations)
            ' '.join(constellations)
            text3 = str(constellations)
            self.consts.setText(text3)

            for const in constellations_lower:
                img = cv2.imread(const+".jpeg")
                cv2.imshow(const, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        moon_phase(moon_side)
        find_constellations(coords, date)

        # Function takes in ratio and outputs a rating
        def get_rating(pollution):
            global bortle
            if pollution < 0.1:  # If ratio is essentially 0
                bortle = 1
                category = "Excellent dark-sky site"
            elif pollution < 0.2:  # less than 5%
                bortle = 2
                category = "Typical truly dark site"
            elif pollution < 0.3:  # less than 15%
                bortle = 3
                category = "Rural sky"
            elif pollution < 0.4:  # less than 35%
                bortle = 4
                category = "Rural/suburban transition"
            elif pollution < 0.5:  # less than 65%
                bortle = 5
                category = "Suburban sky"
            elif pollution < 0.6:  # greater than 65%
                bortle = 6
                category = "Bright suburban sky"
            elif pollution < 0.7:  # greater than 65%
                bortle = 7
                category = "Suburban/urban transition"
            elif pollution < 0.8:  # greater than 65%
                bortle = 8
                category = "City sky"
            else:
                bortle = 9
                category = "Inner-city sky"
            # Return rating back
            types = [bortle, category]
            return types

        def countStars(name):
            img = cv2.imread(name)
            image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blobs_log = blob_log(image_gray, max_sigma=20, num_sigma=10, threshold=.05)

            figure = plt.figure()
            ax = figure.add_subplot(1, 1, 1)

            ax.set_title('Stars Shown')
            ax.imshow(img)

            stars_count = 0
            for pixel in blobs_log:
                y, x, r = pixel
                if r > 2:
                    continue
                ax.add_patch(plt.Circle((x, y), r, color="orange", linewidth=2, fill=False))
                stars_count += 1

            findAverageandDominate()
            text = str(stars_count)
            self.stars.setText(text)

            ax.set_axis_off()
            plt.tight_layout()
            plt.show()
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def findAverageandDominate():
            from colorthief import ColorThief
            img = ios.imread(newname)[:, :, :-1]
            import colorsys

            average = img.mean(axis=0).mean(axis=0)
            color_thief = ColorThief(newname)
            # get the dominant color
            dominant_color = color_thief.get_color(quality=1)
            palette = color_thief.get_palette(color_count=2)
            print(dominant_color, palette)
            hslcolor = colorsys.rgb_to_hls(dominant_color[0], dominant_color[1], dominant_color[2])
            hslcolor = (hslcolor[0] * 360, hslcolor[1] / 255, abs(hslcolor[2]))
            getYellowness(hslcolor)

        def getYellowness(hsl):
            score = (1 / (1 + abs(50 - hsl[0]) * .13)) * .7 + (hsl[1] * 2) * .9 + hsl[2] * .15
            print(score, hsl, 1 / (1 + abs(50 - hsl[0]) * .13) * .7, (1 / (abs(hsl[1] - .5) * 2 + 1)) * .7,
                  hsl[2] * .07)
            bortle_vals = get_rating(score)

            text_rating = str(bortle_vals[0])
            self.rating.setText(text_rating)

            text_place = str(bortle_vals[1])
            self.place.setText(text_place)

        countStars(newname)

        def plotmap():
            map = plt.imread('BlackMarble.png')
            BBox = [-180, 180, -90, 90]
            lat = latit
            lon = longit
            fig, ax = plt.subplots(figsize=(8, 7))
            ax.scatter(lon, lat, zorder=1, c='r', s=50, alpha=.5)
            ax.set_title('Map of light seen from space.')
            ax.set_xlim(-180, 180)
            ax.set_ylim(-90, 90)
            ax.imshow(map, zorder=0, extent=BBox, aspect='equal')
            plt.show()

        plotmap()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(100, 20, 601, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")

        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 550, 260, 16))
        self.label2.setObjectName("label2")

        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(250, 80, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")

        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(340, 110, 100, 32))
        self.button1.setObjectName("button1")

        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(310, 260, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")

        self.label6 = QtWidgets.QLabel(self.centralwidget)
        self.label6.setGeometry(QtCore.QRect(50, 270, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")

        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(470, 270, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")

        self.label9 = QtWidgets.QLabel(self.centralwidget)
        self.label9.setGeometry(QtCore.QRect(50, 320, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label9.setFont(font)
        self.label9.setObjectName("label9")

        self.label8 = QtWidgets.QLabel(self.centralwidget)
        self.label8.setGeometry(QtCore.QRect(240, 410, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label8.setFont(font)
        self.label8.setObjectName("label8")

        self.label10 = QtWidgets.QLabel(self.centralwidget)
        self.label10.setGeometry(QtCore.QRect(50, 370, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label10.setFont(font)
        self.label10.setObjectName("label10")

        self.label11 = QtWidgets.QLabel(self.centralwidget)
        self.label11.setGeometry(QtCore.QRect(470, 370, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label11.setFont(font)
        self.label11.setObjectName("label11")

        self.label12 = QtWidgets.QLabel(self.centralwidget)
        self.label12.setGeometry(QtCore.QRect(470, 320, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label12.setFont(font)
        self.label12.setObjectName("label12")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 550, 271, 16))
        self.label.setObjectName("label")

        self.stars = QtWidgets.QLabel(self.centralwidget)
        self.stars.setGeometry(QtCore.QRect(240, 255, 400, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stars.setFont(font)
        self.stars.setObjectName("stars")

        self.rating = QtWidgets.QLabel(self.centralwidget)
        self.rating.setGeometry(QtCore.QRect(240, 370, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.rating.setFont(font)
        self.rating.setObjectName("rating")

        self.place = QtWidgets.QLabel(self.centralwidget)
        self.place.setGeometry(QtCore.QRect(470, 350, 300, 35))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.place.setFont(font)
        self.place.setObjectName("place")

        self.label13 = QtWidgets.QLabel(self.centralwidget)
        self.label13.setGeometry(QtCore.QRect(60, 190, 67, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label13.setFont(font)
        self.label13.setObjectName("label13")

        self.label14 = QtWidgets.QLabel(self.centralwidget)
        self.label14.setGeometry(QtCore.QRect(60, 220, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label14.setFont(font)
        self.label14.setObjectName("label14")

        self.label15 = QtWidgets.QLabel(self.centralwidget)
        self.label15.setGeometry(QtCore.QRect(330, 190, 120, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label15.setFont(font)
        self.label15.setObjectName("label15")

        self.latitude = QtWidgets.QLineEdit(self.centralwidget)
        self.latitude.setGeometry(QtCore.QRect(150, 190, 113, 21))
        self.latitude.setObjectName("latitude")

        self.longitude = QtWidgets.QLineEdit(self.centralwidget)
        self.longitude.setGeometry(QtCore.QRect(150, 220, 113, 21))
        self.longitude.setObjectName("longitude")

        self.date = QtWidgets.QLineEdit(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(410, 190, 113, 21))
        self.date.setObjectName("season")

        self.button5 = QtWidgets.QPushButton(self.centralwidget)
        self.button5.setGeometry(QtCore.QRect(520, 185, 30, 30))
        self.button5.setObjectName("button5")

        self.consts = QtWidgets.QLabel(self.centralwidget)
        self.consts.setGeometry(QtCore.QRect(50, 330, 800, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.consts.setFont(font)
        self.consts.setObjectName("consts")

        self.label16 = QtWidgets.QLabel(self.centralwidget)
        self.label16.setGeometry(QtCore.QRect(330, 220, 180, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label16.setFont(font)
        self.label16.setObjectName("label16")

        self.visible = QtWidgets.QLineEdit(self.centralwidget)
        self.visible.setGeometry(QtCore.QRect(520, 220, 200, 21))
        self.visible.setObjectName("visible")

        self.button6 = QtWidgets.QPushButton(self.centralwidget)
        self.button6.setGeometry(QtCore.QRect(720, 215, 30, 30))
        self.button6.setObjectName("button6")

        self.label17 = QtWidgets.QLabel(self.centralwidget)
        self.label17.setGeometry(QtCore.QRect(330, 160, 250, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label17.setFont(font)
        self.label17.setObjectName("label17")

        self.side = QtWidgets.QLineEdit(self.centralwidget)
        self.side.setGeometry(QtCore.QRect(550, 160, 113, 21))
        self.side.setObjectName("side")

        self.phase = QtWidgets.QLabel(self.centralwidget)
        self.phase.setGeometry(QtCore.QRect(470, 290, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.phase.setFont(font)
        self.phase.setObjectName("phase")

        self.match = QtWidgets.QLabel(self.centralwidget)
        # 240, 410, 371, 31
        self.match.setGeometry(QtCore.QRect(120, 425, 700, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.match.setFont(font)
        self.match.setObjectName("match")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Python QT Astronomical Observations"))
        self.label2.setText(_translate("MainWindow", "Created By: Dylan Winer and Jake Kasitz"))
        self.label3.setText(_translate("MainWindow", "Press Button Below for Image"))
        self.button1.setText(_translate("MainWindow", "Browse"))
        self.label5.setText(_translate("MainWindow", "Output"))
        self.label6.setText(_translate("MainWindow", "Number of Stars:"))
        self.label7.setText(_translate("MainWindow", "Phase of Moon:"))
        self.label9.setText(_translate("MainWindow", "Constellations Possible:"))
        self.label8.setText(_translate("MainWindow", "Constellation Quality vs Bortle:"))
        self.label10.setText(_translate("MainWindow", "Bortle Scale (1-9):"))
        self.label12.setText(_translate("MainWindow", "Type of Sky:"))
        self.label.setText(_translate("MainWindow", "Planet Idea Credit: Katerina Patounakis"))
        self.label13.setText(_translate("MainWindow", "Latitude:"))
        self.label14.setText(_translate("MainWindow", "Longitude:"))
        self.label15.setText(_translate("MainWindow", "Season:"))
        self.label16.setText(_translate("MainWindow", "Constellations Visible?:"))
        self.label17.setText(_translate("MainWindow", "Side of moon? (L/R/None):"))

        self.button1.clicked.connect(self.browse_1)
        self.button5.clicked.connect(self.find_date)
        self.button6.clicked.connect(self.analyze_const)

    def browse_1(self, astronomer):
        self.open_dialog_box()

    def browse_2(self, astronomer):
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        print(filename)
        path = filename[0]
        print(path)
        global newname
        newname = os.path.basename(path)
        print("Newname", newname)

    def find_date(self):
        global coords
        global lati
        global longi
        global moon_side

        lati = str(self.latitude.text())
        lati = float(lati)
        print("lati", lati)

        longi = str(self.longitude.text())
        longi = float(longi)

        coords = (lati, longi)
        date = str(self.date.text())
        moon_side = str(self.side.text())
        self.astronomer(newname, coords, date, moon_side)

    def analyze_const(self):
        print("Analyzed constellations")
        bright = ["orion", "taurus", "canis major", "centaurus", "scorpius", "pegasus", "lyra",
                  "ophiuchus", "eridanus", "bootes", "hydra"]
        middle = ["leo", "virgo", "cygnus", "aquila", "hercules", "andromeda", "cetus", "perseus"]
        low = ["ursa minor", "gemini", "pisces", "sagittarius", "aquarius", "capricornus", "cancer", "crater"]

        # global visibles
        visibles = str(self.visible.text())
        print("Visibles are", visibles)

        visibles_list = visibles.split(",")
        print("Visibles list", visibles_list)
        if len(visibles_list) == 0:
            max_quality = 0

        qualities = []
        for constellation in visibles_list:
            if constellation in bright:
                qualities.append(1)
            elif constellation in middle:
                qualities.append(2)
            elif constellation in low:
                qualities.append(3)

        max_quality = max(qualities)
        print("Max quality", max_quality)
        if max_quality == 3:
            qual = "very high"
            print("Quality is very high")
        elif max_quality == 2:
            qual = "high"
            print("Quality is high")
        elif max_quality == 1:
            qual = "medium"
            print("Quality is medium")
        elif max_quality == 0:
            qual = "low"
            print("Quality is bad")

        if 7 <= bortle <= 9:
            bortle_qual = "low"
        elif 5 <= bortle < 7:
            bortle_qual = "medium"
        elif 3 <= bortle < 5:
            bortle_qual = "high"
        elif 1 <= bortle < 3:
            bortle_qual = "very high"

        if max_quality == 0 and 7 <= bortle <= 9:
            self.match.setText("Quality matches")
        elif max_quality == 1 and 5 <= bortle < 7:
            self.match.setText("Quality matches")
        elif max_quality == 2 and 3 <= bortle < 5:
            self.match.setText("Quality matches")
        elif max_quality == 3 and 1 <= bortle < 3:
            self.match.setText("Quality matches")
        else:
            match_text = "Quality of", qual, "does not match bortle rating qual of", bortle_qual
            self.match.setText(str(match_text))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

