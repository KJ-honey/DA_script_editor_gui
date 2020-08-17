import sys
from PyQt5.QtWidgets import QMainWindow,QAction,QApplication,qApp,QFileDialog,QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import scriptForGui as myfunc

pathDir=os.getcwd()
form_class = uic.loadUiType(pathDir+'\\gui.ui')[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.firstFileNumber=3520
        self.statusBar().showMessage('Ready')

        self.btn_save.setDisabled(True)
        self.btn_insert.setDisabled(True)
        self.actioninsert.setDisabled(True)
        self.actionSave.setDisabled(True)
        self.actionSaveAs.setDisabled(True)
        self.actionSave_ID3841.setDisabled(True)
        self.actioninsert.setDisabled(True)
        self.actionNextText.setDisabled(True)
        self.actionPrevText.setDisabled(True)
        #self.action.setDisabled(True)
        #ListWidget의 시그널
        self.fileList.itemClicked.connect(self.clicked_script_name)
        self.fileList.currentItemChanged.connect(self.clicked_script_name)
        self.scriptsList.itemClicked.connect(self.clicked_script)
        self.scriptsList.currentItemChanged.connect(self.clicked_script)
        #버튼에 기능 연결
        self.btn_open.clicked.connect(self.clicked_btn_open)
        self.btn_insert.clicked.connect(self.insertText)
        self.btn_save.clicked.connect(self.clicked_btn_save)


        #액션 연결
        self.actionopen.triggered.connect(self.clicked_btn_open)
        self.actionSave.triggered.connect(self.clicked_btn_save)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionOpen_ID3841_as.triggered.connect(self.clicked_btn_open_spsi)
        self.actionSave_ID3841.triggered.connect(self.clicked_save_spsi)
        self.actioninsert.triggered.connect(self.insertText)
        self.actionNextText.triggered.connect(self.Next_text)
        self.actionPrevText.triggered.connect(self.Prev_text)
        self.actionexit.triggered.connect(qApp.quit)
        self.actionExtract_bin_from_ISO.triggered.connect(self.clicked_extract_iso)
        self.actionImport_bin_to_ISO.triggered.connect(self.clicked_import_iso)
        self.statusBar()

    #ListWidget의 시그널에 연결된 함수들
    def clicked_extract_iso(self):
        binfilter="bin files (*.bin);;All files (*.*)"
        isofilter="iso files (*.iso);;All files (*.*)"
        pathIso=QFileDialog.getOpenFileName(self,'Open to...','./',isofilter,"iso files (*.iso)")[0]
        if pathIso=='':return 0
        pathBin=QFileDialog.getSaveFileName(self,'Save as...','./',binfilter,"bin files (*.bin)")[0]
        if pathBin=='':return 0
        myfunc.dataExtractorForISO(pathIso,pathBin)
    def clicked_import_iso(self):
        myfilter="iso files (*.iso);;All files (*.*)"
        binfilter="bin files (*.bin);;All files (*.*)"
        pathBin=QFileDialog.getOpenFileName(self,'Open to...','./',binfilter,"bin files (*.bin)")[0]
        if pathIso=='':return 0
        pathIso=QFileDialog.getSaveFileName(self,'Save as...','./',isofilter,"iso files (*.iso)")[0]
        if pathBin=='':return 0
        myfunc.dataImportForISO(pathIso,pathBin)

    def clicked_save_spsi(self):
        if self.switcgMode!='spsi':
            self.statusBar().showMessage('This is not a ID03831')
            return
        myfunc.IDspsi_Import(self.inf,self.texts)
        #print(self.texts[0])
        self.statusBar().showMessage('Save complete')
        QMessageBox.information(self, 'Information', "Save complete", QMessageBox.Ok,QMessageBox.Ok)

    def clicked_btn_save(self): 
        if self.switcgMode!='script':
            self.statusBar().showMessage('This is not a scriptfile')
            return       
        myfunc.script_import_gui(self.headerList,self.dialogNum,self.texts,self.inf)
        self.statusBar().showMessage('Save complete')
        QMessageBox.information(self, 'Information', "Save complete", QMessageBox.Ok,QMessageBox.Ok)

    def save_as(self):        
        if self.switcgMode!='script':
            self.statusBar().showMessage('This is not a scriptfile')
            return       
        myfilter="Bin files (*.bin);;All files (*.*)"
        savename=QFileDialog.getSaveFileName(self,'Save as...','./',myfilter,"Bin files (*.bin)")[0]
        if savename=='':return 0
        outf=open(savename,'wb+')
        self.inf.seek(0)
        outf.write(self.inf.read())
        outf.seek(0)
        myfunc.script_import_gui(self.headerList,self.dialogNum,self.texts,outf)
        outf.close()
        self.statusBar().showMessage('Save complete')
        QMessageBox.information(self, 'Information', "Save complete", QMessageBox.Ok,QMessageBox.Ok)
        
    def insertText(self):
        self.typingText=self.editText.toPlainText()
        self.currentText.setPlainText(self.typingText)
        currentRow=self.scriptsList.currentRow()
        self.scriptsList.takeItem(currentRow)
        if self.switcgMode=='spsi':
            self.scriptsList.insertItem(currentRow,self.typingText)
            self.texts[currentRow]=self.typingText
            self.statusBar().showMessage('Insert complete')

        else:
            currentRow=str(currentRow)
            for j in range(4):
                if len(str(currentRow))<3:
                    currentRow='0'+currentRow
            self.scriptsList.insertItem(int(currentRow),currentRow+'. '+self.typingText)
            iNum=sum(self.dialogNum[0:self.scriptName])+int(currentRow)

            self.texts[iNum]=myfunc.str_to_bin(self.typingText,1)
            self.statusBar().showMessage('Insert complete')

    def clicked_script_name(self):
        while True:
            try:
                self.scriptName=int(self.fileList.currentItem().text())-self.firstFileNumber
                break
            except:
                break
        num=0
        self.currentText.clear()
        self.editText.clear()
        self.scriptsList.clear()
        self.speakerName.clear()
        self.listName=[]
        if self.switcgMode=='spsi':
            for i in range(len(self.texts)):
                self.scriptsList.addItem(self.texts[i])
        else:
            for i in range(self.dialogNum[self.scriptName]):
                num=str(num)
                for j in range(4):
                    if len(str(num))<3:
                        num='0'+num
                self.iNum=i+sum(self.dialogNum[0:self.scriptName])
                self.scriptsList.addItem(num+'. '+myfunc.str_to_bin(self.texts[self.iNum],2))
                self.listName.append(self.speakerAndDialogs[0][self.iNum])

                num=int(num)+1
            self.scriptsList.setCurrentRow(0)
            self.statusBar().showMessage('Script number %d is loaded'%(self.scriptName+self.firstFileNumber))
    
    def clicked_script(self):
        if self.switcgMode=='spsi':
            while True:
                try:
                    self.itemscript=self.scriptsList.currentItem().text()
                    break
                except :
                    break
                    
        else:
            while True:
                try:
                    self.itemscript=self.scriptsList.currentItem().text()[5:]
                    self.itemNumber=int(self.scriptsList.currentItem().text()[0:3])
                    #print(self.scriptName) #스크립트 번호반환
                    #print(self.scriptsList.currentItem().text()[0:3]) # 현재 나열된 텍스트의 제일앞 번호 3자리
                    break
                except :
                    break
            #for i in self.texts:
                #print(myfunc.str_to_bin(i,2))
            num=0
            #self.text.clear()
            currentName=self.listName[self.itemNumber]
            self.speakerName.setPlainText(currentName)
            #print(self.listName[self.itemNumber])
        self.currentText.setPlainText(self.itemscript)
        self.editText.setPlainText(self.itemscript)
        #print(self.currentText.toPlainText())

    #버튼 함수
    def clicked_btn_open(self):
        try:self.inf.close()
        except:pass
        self.currentText.clear()
        self.editText.clear()
        self.scriptsList.clear()
        self.speakerName.clear()
        self.fileList.clear()
        self.headerList=[]
        self.dialogNum=[]
        self.texts=[]
        self.switcgMode='script'

        binfilter="bin files (*.bin);;All files (*.*)"
        self.filename = QFileDialog.getOpenFileName(self,'Open to...','./',binfilter,"bin files (*.bin)")[0]
        #self.filename='onlytext_test1.bin'
        if self.filename=='':return 0
        self.inf = open(self.filename,'rb+')
        self.data=self.inf.read()

        self.headerList=myfunc.find_header(b'\x45\x54\x44\x46',self.data)
        self.dialogNum=myfunc.dialog_num(self.headerList,self.data)

        for i in range(len(self.dialogNum)):
            self.fileList.addItem(str(i+self.firstFileNumber))
        self.speakerAndDialogs=myfunc.script_extract(self.headerList,self.dialogNum,self.inf) 
        self.texts=self.speakerAndDialogs[1]
        self.fileList.setCurrentRow(0)
        
        self.btn_save.setEnabled(True)
        self.btn_insert.setEnabled(True)
        self.actioninsert.setEnabled(True)
        self.actionSave.setEnabled(True)
        self.actionSaveAs.setEnabled(True)
        self.actioninsert.setEnabled(True)
        self.actionNextText.setEnabled(True)
        self.actionPrevText.setEnabled(True)

    def clicked_btn_open_spsi(self):
        try:self.inf.close()
        except:pass
        self.switcgMode='spsi'
        self.fileList.clear()
        self.texts=[]
        self.filename = QFileDialog.getOpenFileName(self)[0]
        if self.filename=='':return 0
        #self.filename = 'ID03841'
        self.fileList.addItem(self.filename)
        self.inf=open(self.filename,'rb+')
        self.texts=myfunc.IDspsi_Extract(self.inf)
        #self.scriptslist.addItem()
        self.fileList.setCurrentRow(0)

    def Next_text(self):
        self.scriptsList.setCurrentRow(self.scriptsList.currentRow()+1)
    def Prev_text(self):
        self.scriptsList.setCurrentRow(self.scriptsList.currentRow()-1)

if __name__ == "__main__" :
    print("Start gui for dgmAd psp scripter")
    
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()