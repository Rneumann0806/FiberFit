import sys
sys.path.append("/fiberfit/")
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


class Ui_MainWindow(object):
    """
    Defines the view of the main FiberFit UI (the first thing you see when you run FiberFit
    """
    def setupUi(self, MainWindow, heigth, width):
        """
        Sets up all of the GUI components of the main FiberFit UI.
        Created by PyQt5 UI code generator 5.4
        :param MainWindow: instance of fiberfit.fft_mainWindow
        :param heigth: height of the screen
        :param width: width of the screen
        :return: none

        """

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(5.3*self.dpi, 0.53*self.dpi)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(width, heigth))
        MainWindow.setAutoFillBackground(False)

        fSize = .07*self.dpi

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.midGrid = QtWidgets.QGridLayout()
        self.midGrid.setObjectName("midGrid")

        self.selectImgBox = QtWidgets.QComboBox(self.centralwidget)
        self.selectImgBox.AdjustToContents
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectImgBox.sizePolicy().hasHeightForWidth())
        self.selectImgBox.setSizePolicy(sizePolicy)
        self.selectImgBox.setMinimumSize(QtCore.QSize(.15*width, fSize*3))
        self.selectImgBox.setMaximumSize(QtCore.QSize(.15*width, fSize*3))
        self.selectImgBox.setObjectName("selectImgBox")
        self.midGrid.addWidget(self.selectImgBox, 0, 0, 1, 1)

        # Progress bar
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimum(0)
        self.progressBar.setMinimumSize(QtCore.QSize(0.1*width, 2*fSize))
        self.progressBar.setMaximumSize(QtCore.QSize(0.1*width, 2*fSize))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()

        spacerItem0 = QtWidgets.QSpacerItem(0.08*width, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.midGrid.addItem(spacerItem0, 0, 3, 1, 1)

        # sigma label
        self.sigLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont("Times", fSize)
        self.sigLabel.setFont(font)
        self.sigLabel.setObjectName("sigLabel")
        self.sigLabel.setToolTip("Standard Deviation Of Fiber Distribution")
        self.midGrid.addWidget(self.sigLabel, 0, 6, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(0.08*width, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.midGrid.addItem(spacerItem, 0, 11, 1, 1)

        # R^2 label
        self.RLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont("Times", fSize)
        font.setItalic(False)
        self.RLabel.setFont(font)
        self.RLabel.setTextFormat(QtCore.Qt.AutoText)
        self.RLabel.setObjectName("RLabel")
        self.RLabel.setToolTip("Coefficient of Determination")
        self.midGrid.addWidget(self.RLabel, 0, 10, 1, 1)

        wWidth = 0.04*width
        spacerItem1 = QtWidgets.QSpacerItem(wWidth, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.midGrid.addItem(spacerItem1, 0, 5, 1, 1)

        # mu label
        self.muLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont("Times", fSize)
        self.muLabel.setFont(font)
        self.muLabel.setObjectName("muLabel")
        self.muLabel.setToolTip("Mean Fiber Orientation")
        self.midGrid.addWidget(self.muLabel, 0, 4, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(wWidth, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.midGrid.addItem(spacerItem2, 0, 7, 1, 1)

        #k label
        self.kLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont("Times", fSize)
        font.setItalic(False)
        self.kLabel.setFont(font)
        self.kLabel.setTextFormat(QtCore.Qt.AutoText)
        self.kLabel.setObjectName("kLabel")
        self.kLabel.setToolTip("Fiber Dispersion Parameter")
        self.midGrid.addWidget(self.kLabel, 0, 8, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(wWidth, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.midGrid.addItem(spacerItem3, 0, 9, 1, 1)
        self.gridLayout.addLayout(self.midGrid, 1, 0, 1, 1)

        # figure widget is the widget that contains 4 figures from the FiberFit UI
        self.figureWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.figureWidget.sizePolicy().hasHeightForWidth())
        self.figureWidget.setSizePolicy(sizePolicy)
        self.figureWidget.setObjectName("figureWidget")
        self.figureLayout = QtWidgets.QGridLayout(self.figureWidget)
        self.figureLayout.setObjectName("figureLayout")
        self.figureWidget.setMinimumSize(QtCore.QSize(.4*width, .1*heigth))
        self.figureWidget.setMaximumSize(QtCore.QSize(width, heigth))
        self.gridLayout.addWidget(self.figureWidget, 2, 0, 1, 1)

        self.topGrid = QtWidgets.QGridLayout()
        self.topGrid.setObjectName("topGrid")

        spacerItem3 = QtWidgets.QSpacerItem(wWidth, fSize, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.topGrid.addItem(spacerItem3, 0, 6, 1, 1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())

        # progress bar
        self.barWidget = QtWidgets.QWidget()
        self.barWidget.setObjectName("barWidget")
        self.barWidget.setSizePolicy(sizePolicy)
        # layout for the progress bar
        self.gridPLayout = QtWidgets.QGridLayout(self.barWidget)
        self.gridPLayout.setContentsMargins(0, 0, 0, 0)
        self.gridPLayout.setObjectName("gridLayout")
        self.gridPLayout.addWidget(self.progressBar, 0, 0, 1, 1)
        self.topGrid.addWidget(self.barWidget, 0, 5, 1, 1)

        # clear button
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.clearButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.clearButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.find_data_file('clearButton.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon)
        self.clearButton.setIconSize(QtCore.QSize(0.0104*width, 0.0104*width))
        self.clearButton.setObjectName("clearButton")
        self.topGrid.addWidget(self.clearButton, 0, 4, 1, 1)
        self.clearButton.setToolTip("Clear Images")

        # export button
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy)
        self.exportButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.exportButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.exportButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.find_data_file('export.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportButton.setIcon(icon1)
        self.exportButton.setIconSize(QtCore.QSize(0.013*width, 0.013*width))
        self.exportButton.setObjectName("exportButton")
        self.exportButton.setToolTip("Export")
        self.topGrid.addWidget(self.exportButton, 0, 2, 1, 1)

        # open images/load button
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        self.loadButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.loadButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.loadButton.setAcceptDrops(False)
        self.loadButton.setAutoFillBackground(False)
        self.loadButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.find_data_file('open.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadButton.setIcon(icon2)
        self.loadButton.setIconSize(QtCore.QSize(0.013*width, 0.013*width))
        self.loadButton.setObjectName("loadButton")
        self.loadButton.setToolTip("Open")
        self.topGrid.addWidget(self.loadButton, 0, 0, 1, 1)

        # start button
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.startButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.startButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.startButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.find_data_file('start-icon.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon3)
        self.startButton.setIconSize(QtCore.QSize(0.0104*width, 0.0104*width))
        self.startButton.setObjectName("startButton")
        self.startButton.setToolTip("Run")
        self.topGrid.addWidget(self.startButton, 0, 1, 1, 1)

        # settings button
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsButton.sizePolicy().hasHeightForWidth())
        self.settingsButton.setSizePolicy(sizePolicy)
        self.settingsButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.settingsButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.settingsButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.settingsButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.find_data_file('settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingsButton.setIcon(icon4)
        self.settingsButton.setIconSize(QtCore.QSize(0.0104*width, 0.0104*width))
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.setToolTip("Settings")
        self.topGrid.addWidget(self.settingsButton, 0, 3, 1, 1)

        # next image button
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.nextButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        font = QtGui.QFont("Times", fSize)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setToolTip("Next Image")
        self.topGrid.addWidget(self.nextButton, 0, 8, 1, 1)

        # previous image button
        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy)
        self.prevButton.setToolTip("Previous Image")
        self.prevButton.setMinimumSize(QtCore.QSize(0.02*width, 0.018*width))
        self.prevButton.setMaximumSize(QtCore.QSize(0.02*width, 0.018*width))
        font = QtGui.QFont("Times", fSize)
        self.prevButton.setFont(font)
        self.prevButton.setObjectName("prevButton")

        self.topGrid.addWidget(self.prevButton, 0, 7, 1, 1)
        self.gridLayout.addLayout(self.topGrid, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0.16*width, 0.0057*width))
        self.menubar.setObjectName("menubar")
        self.menuFiberfit = QtWidgets.QMenu(self.menubar)
        self.menuFiberfit.setObjectName("menuFiberfit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFiberfit.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Sets up appropriate text values for the UI.
        :param MainWindow: instance of FiberFit.fft_mainWindow
        :return: none
        """
        MainWindow.setWindowTitle("FiberFit")
        self.RLabel.setText('R' + u"\u00B2" + " = ")
        self.kLabel.setText("k = ")
        self.muLabel.setText("μ =")
        self.nextButton.setText("→")
        self.prevButton.setText("←")
        self.menuFiberfit.setTitle("Fiberfit")
        self.sigLabel.setText("σ =")

    def find_data_file(self, filename):
        """
        Allows for dynamic loading of the picture icons. cx_Freeze (framework I am using to make app executable)
        will use this to populate all of the buttons that have icons.
        :param filename: name of the picture w/o a path
        :return: none
        """
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.dirname('../../resources/images/')
        return os.path.join(datadir, filename)