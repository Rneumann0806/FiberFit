import sys
sys.path.append("/fiberfit/")
from src.fiberfit_gui import export_window
from src.fiberfit_control.support import img_model

from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QFileDialog
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSizeF
from PyPDF2 import PdfFileMerger as merger
from PyQt5 import QtWebEngineWidgets
import csv
# from orderedset import OrderedSet
import pathlib
import os
import numpy as np
import collections

class OrderedSet(collections.MutableSet):
    """
    # Recipe from http://code.activestate.com/recipes/576694/
    Banana banana
    """

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def __getstate__(self):
        if len(self) == 0:
            # The state can't be an empty list.
            # We need to return a truthy value, or else
            # __setstate__ won't be run.
            #
            # This could have been done more gracefully by always putting
            # the state in a tuple, but this way is backwards- and forwards-
            # compatible with previous versions of OrderedSet.
            return (None,)
        else:
            return list(self)

    def __setstate__(self, state):
        if state == (None,):
            self.__init__([])
        else:
            self.__init__(state)

    def discard(self, key):
        if key in self.map:
            key, prev, nxt = self.map.pop(key)
            prev[2] = nxt
            nxt[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    # pylint: disable=arguments-differ
    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

class ReportDialog(QDialog, export_window.Ui_Dialog):
    """ Summary of ReportDialog.

    Represents a pop-up dialog when user presses "Export" button. Dialog contains a preview of the report containing
    values of "mu", "k", "R^2" and the replica of FiberFit main window's when a sample has been processed.

    Attributes:
        - do_print is a signal sent when either Save or Save All button are pressed.
        - do_excel is a signal starting the process of exporting results into an .csv format
        - sendDataList is a signal that sends a list containing already exported images back to FiberFit.
        - data_list is a list representing already exported images
        - screen_dim stores a screen dimension
        - document is an instance of QTextDocument that
       TODO: add other attributes.
    """
    do_print = pyqtSignal()
    do_excel = pyqtSignal()
    do_RawCSV = pyqtSignal()
    sendDataList = pyqtSignal(list)

    def __init__(self, fft_mainWindow,parent=None, screenDim=None):

        super(ReportDialog, self).__init__(parent)
        self.fft_mainWindow=fft_mainWindow
        self.dataList = []
        self.setupUi(self, screenDim)
        self.screenDim = screenDim
        self.document = QTextDocument()
        #list that keeps track of only selected images
        self.list = []
        #list that contains all of the stored images
        self.wholeList = OrderedSet()
        self.savedfiles = None
        self.currentModel = None
        # settings
        self.uCut = 0
        self.lCut = 0
        self.angleInc = 0
        self.radStep = 0
        #  states
        """
        0 -> single
        1 -> multiple
        2 -> append
        """
        self.isReport = True
        self.isSummary = False
        self.isRaw = False
        self.reportOption = 2
        self.merger = merger()
        # printer
        self.printer = QPrinter(QPrinter.PrinterResolution)
        # Signals and slots:
        self.do_excel.connect(self.exportExcel)
        self.do_RawCSV.connect(self.exportRawCSV)
        self.webView = QtWebEngineWidgets.QWebEngineView()

        # self.checkBox_report.stateChanged.connect(self.topLogicHandler)
        self.checkBox_summary.stateChanged.connect(self.topLogicHandler)
        self.checkBox_RawData.stateChanged.connect(self.topLogicHandler)

        self.radio_multiple.toggled.connect(self.toggleHandler)
        self.radio_single.toggled.connect(self.toggleHandler)
        self.radio_append.toggled.connect(self.toggleHandler)

        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.exportHandler)
        self.do_print.connect(self.print)
        self.rejected.connect(self.resetOptions)
        self.topLogicHandler()

    def resetOptions(self):
        self.checkBox_summary.setChecked(False)
        self.radio_append.setChecked(True)
        self.radio_multiple.setChecked(False)
        self.radio_single.setChecked(False)

    def exportHandler(self):
        # if self.isSummary and self.isReport is False:
        #     self.saveas()
        # elif (self.reportOption == 0 or self.reportOption == 2 or self.reportOption == 1) and self.isSummary is False:
        #     self.saveas()
        # elif self.isSummary and self.isReport:
        #     self.saveas()
        if (self.isSummary or self.reportOption == 0 or self.reportOption==1 or self.reportOption==2 or self.isReport or self.isRaw):
            self.saveas()

    def toggleHandler(self):
        if self.radio_single.isChecked():
            self.reportOption = 0
            self.isReport = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_multiple.isChecked():
            self.reportOption = 1
            self.isReport = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_append.isChecked():
            self.reportOption = 2
            self.isReport = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_none.isChecked():
            self.reportOption = -1
            self.isReport = False
            if (not self.checkBox_summary.isChecked()) and (not self.checkBox_RawData.isChecked()):
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def topLogicHandler(self):

        if self.checkBox_summary.isChecked():
            self.isSummary = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.checkBox_summary.isChecked() is False:
            self.isSummary = False
            if (self.radio_none.isChecked()) and self.checkBox_RawData.isChecked() is False:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        if self.checkBox_RawData.isChecked():
            self.isRaw = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.checkBox_RawData.isChecked() is False:
            self.isRaw = False
            if (self.radio_none.isChecked()) and self.checkBox_summary.isChecked() is False:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    @pyqtSlot()
    def exportExcel(self):
        if self.dataList.__len__() == 0:
            self.dataList.append(
                [self.wholeList.__getstate__()[0].filename.stem,
                 self.uCut,
                 self.lCut,
                 self.radStep,
                 self.angleInc,
                 self.wholeList.__getstate__()[0].sig,
                 self.wholeList.__getstate__()[0].th,
                 self.wholeList.__getstate__()[0].k,
                 self.wholeList.__getstate__()[0].R2,
                 self.wholeList.__getstate__()[0].timeStamp])
        temp = []
        for i in range(0, self.wholeList.__len__()):
            temp.append(self.wholeList.__getstate__()[i])
        for i in range(0, len(self.dataList)):
            found = False
            for j in range(0, len(temp)):
                # One image from list is at most can equal to one another image from temp
                if found is False and self.dataList[i][0] == temp[j].filename.stem:
                    self.dataList.remove(self.dataList[i])
                    self.dataList.insert(i, [temp[j].filename.stem,
                                             self.uCut,
                                             self.lCut,
                                             self.radStep,
                                             self.angleInc,
                                             round(temp[j].sig[0], 2),
                                             round(temp[j].th, 2),
                                             round(temp[j].k, 2),
                                             round(temp[j].R2, 2),
                                             temp[j].timeStamp])
                    temp.remove(temp[j])
                    found = True
        for k in range(0, len(temp)):
            self.dataList.append([temp[k].filename.stem,
                                  self.uCut,
                                  self.lCut,
                                  self.radStep,
                                  self.angleInc,
                                  round(temp[k].sig[0], 2),
                                  round(temp[k].th, 2),
                                  round(temp[k].k, 2),
                                  round(temp[k].R2, 2),
                                  temp[k].timeStamp])
        with open(str(self.savedfiles.parents[0]) + '/summary.csv', 'w', newline='') as csvfile:
            a = csv.writer(csvfile)
            a.writerow(['Name', 'LowerCut', 'UpperCut', 'RadialStep', 'AngleIncrement', 'Sig', 'Mu', 'K', 'R^2', 'Time'])
            a.writerows(self.dataList)
        self.fft_mainWindow.dataList = self.dataList

    @pyqtSlot()
    def exportRawCSV(self):
        for i in range(len(self.wholeList)):
            with open(os.path.join(str(self.savedfiles.parents[0]), self.wholeList.__getstate__()[i].filename.stem+'.csv'), 'w', newline='') as csvfile:
                a = csv.writer(csvfile)
                a.writerow([str(self.wholeList.__getstate__()[i].filename.stem), str(self.wholeList.__getstate__()[i].timeStamp)])
                a.writerow(['Theta (radians)', 'NormalizedPS'])
                for ii in range(len(self.wholeList.__getstate__()[i].Theta1RadFinal)):
                    a.writerow([self.wholeList.__getstate__()[i].Theta1RadFinal[ii], self.wholeList.__getstate__()[i].normPower[ii]])

    def saveas(self):
        """
        Pops out a dialog allowing user to select where to save the image.
        """
        dialog = QFileDialog()
        if (self.reportOption == 0):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export", self.currentModel.filename.stem)[0])
            self.close()
        elif (self.reportOption == 1):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Image Name")[0])
            self.close()
        elif (self.reportOption == 2):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Report")[0])
            self.close()
        if (self.isSummary and not self.isReport) or (self.isRaw and not self.isReport):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "SummaryTable")[0])
        self.printerSetup()
        if (self.isReport == True):
            self.do_print.emit()
        if self.isSummary == True:
            self.do_excel.emit()
        if self.isRaw == True:
            self.do_RawCSV.emit()

    def print(self):
        """
        Checks which button sent a signal. Based on that it either prints all images or just a single specific image.
        """
        if (self.reportOption == 1):
            for model in self.wholeList:
                self.document.setHtml(self.createHtml(model, forPrinting=True))
                self.printer.setOutputFileName(
                    self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf')
                # self.document.setPageSize(QSizeF(self.printer.pageRect().size()))
                self.document.print(self.printer)
        elif (self.reportOption == 0):
            # self.document.setPageSize(QSizeF(self.printer.pageRect().size()))
            self.document.print(self.printer)

        elif (self.reportOption == 2):
            self.merger = merger()
            input_list = []
            for model in self.wholeList:
                self.document.setHtml(self.createHtml(model, forPrinting=True))
                name = self.savedfiles.__str__() + '.pdf'
                print(name)
                self.printer.setOutputFileName(
                    self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf')
                # self.document.setPageSize(QSizeF(self.printer.pageRect().size()))
                self.document.print(self.printer)
                input = open(self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf', "rb")
                self.merger.append(input)
                input_list.append([input, self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf'])

            out = open(name, "wb")
            self.merger.write(out)
            self.merger.close()

            #Close and remove individual sample PDFs. Separate loop because they are needed to make the merged PDF. -Erica Neumann
            for PDF_input in input_list:
                PDF_input[0].close()
                os.remove(PDF_input[1])

    def printerSetup(self):
        """
        Sets up default instructions for printer.
        """
        self.printer.setPageSize(QPrinter.Letter)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setFullPage(True)
        self.printer.setOutputFileName(str(self.savedfiles)+".pdf")

    def createHtml(self, model, forPrinting):
        """
        Creates html-based report that shows the basic information about the sample.
        """
        # for printing
        if forPrinting:
            print(os.getcwd())
            wid = int(self.fft_mainWindow.dpi)*3 # make all images 3 inches in width
            html = """
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='support/ntm_style.css') }}"/>
            </head>
            <body>
                <p> Image Name: {name} </p> <p> μ: {th}° </p>
                <p>k: {k} </p>
                <p>R^2: {R2} </p>
                <p>σ: {sig}°</p>
                <br>
                <table>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedOrgImg}" width = {wid} /></td>
                        <td> <img src ="data:image/png;base64,{encodedLogScl}" width = {wid}/></td>
                    </tr>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedAngDist}" width = {wid} /></td>
                        <td> <img src = "data:image/png;base64,{encodedCartDist}" width = {wid} /></td>
                    </tr>
                </table>
                <p><br><br>
                    {date}
                </p>
            </body>
        </html>
        """.format(name=model.filename.stem, th=round(model.th, 2), k=round(model.k, 2), R2=round(model.R2, 2),
                   sig = round(model.sig[0], 2),
                   encodedOrgImg=model.orgImgEncoded.translate('bn\''),
                   encodedLogScl=model.logSclEncoded.translate('bn\''),
                   encodedAngDist=model.angDistEncoded.translate('bn\''),
                   encodedCartDist=model.cartDistEncoded.translate('bn\''),
                   wid=str(wid),
                   date=model.timeStamp)
            return html

    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        """
        Makes report for an image that was active when user pressed Export button.
        """
        self.webView.setHtml(self.createHtml(model, False))
        self.document.setHtml(self.createHtml(model, True))
        self.currentModel = model
        self.show()

    @pyqtSlot(list, list, OrderedSet, float, float, float, float)
    def receiver(self, selectedImgs, dataList, imgList, uCut, lCut, radStep, angleInc):
        """
        Received an information from FiberFit application with necessary report data.
        """
        self.dataList = dataList
        self.list = selectedImgs
        self.wholeList = imgList
        self.uCut = uCut
        self.lCut = lCut
        self.radStep = radStep
        self.angleInc = angleInc

