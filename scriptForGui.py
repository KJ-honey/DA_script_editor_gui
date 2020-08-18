import os
import sys
import pandas as pd
import re
def main():
    print(str_to_bin("Test str2bin mode 1 : 아아아아뷁",1))
    filename1='onlytext_test1.bin'
    filename2='testExtBin.bin'
    test(filename1)
    test(filename2)    
def test(fn):
        switcgMode='script'
        headerList=[]
        dialogNum=[]
        texts=[]

        #filename = QFileDialog.getOpenFileName(self)[0]
        filename=fn
        inf = open(filename,'rb+')
        data=inf.read()

        headerList=find_header(b'\x45\x54\x44\x46',data)
        dialogNum=dialog_num(headerList,data)


        speakerAndDialogs=script_extract(headerList,dialogNum,inf) 
        inf.close()
        testStr=speakerAndDialogs[1][1000]
        print(testStr)
        print(str_to_bin(testStr,2))
        
def dataExtractorForISO(pathIso,pathFile):
    isoFp=open(pathIso,'rb')
    isoFp.seek(379666432)
    data=isoFp.read(2034592)
    isoFp.close()
    
    saveFp=open(pathFile,'wb')
    saveFp.write(data)
    saveFp.close()
def dataImportForISO(pathIso,pathFile):
    fpIso = open(pathIso,'rb+')
    fpFile = open(pathFile,'rb')
    
    data = fpFile.read()
    fpFile.close()

    fpIso.seek(379666432)
    fpIso.write(data)
    fpIso.close()
    
def speakerNameIntToStr(Int,df): 
    try:
        name = df.loc[Int,'name']
        Int=str(Int)
        Int=Int.replace(Int,name)
    except:
        Int=str(Int)
    return Int
def IDspsi_GetlistOffset_ex(fp):
    numOfScripts=278
    OffsetStartOffset = 16
    fp.seek(OffsetStartOffset,0)
    listOffset = []
    for i in range(numOfScripts):
        Offset=int.from_bytes(bytes=fp.read(2),byteorder='little')
        listOffset.append(Offset)
        fp.seek(2,1)
    return listOffset
def IDspsi_GetlistScripts_ex(fp,listOffset):
    numOfScripts=278
    OffsetStartScript=1128
    listScripts=[]
    fp.seek(OffsetStartScript,0)
    OffsetEndOfScript=0

    for i in range(numOfScripts):
        fp.seek(listOffset[i])    #대사 시작점으로 이동
        while True:
            try:
                if numOfScripts-1==i:              #else에서 행하는 i+1이 루프의 마지막 차례에서 i범위를 초과함으로 예외처리
                    finishData=fp.read(100)
                    length=finishData.find(b'\x00')
                    text=finishData[0:length]
                    text=str_to_bin(text,2)
                else:
                    length=listOffset[i+1]-listOffset[i]-1
                    text=fp.read(length)
                    length2=text.find(b'\x00')
                    if length2!=-1:length=length2
                    else : length=length
                    text=text[0:length]
                    text=str_to_bin(text,2)
                listScripts.append(text)
                break
            except IndexError:break
    return listScripts

def IDspsi_Extract(fp):
    listOffset=IDspsi_GetlistOffset_ex(fp)
    return IDspsi_GetlistScripts_ex(fp,listOffset)

def IDspsi_SetOffset_im(fp,listScripts):
    numOfScripts=278
    OffsetStartOffset = 16
    OffsetStartScript=1128
    fp.seek(OffsetStartOffset,0)

    for i in range(numOfScripts):
        if i!=0:
            writeOffset=lengths
            fp.write(int.to_bytes(writeOffset,2,'little'))
        else : 
            firstOffset=int.from_bytes(bytes=fp.read(2),byteorder='little')
            fp.seek(-2,1)
            fp.write(int.to_bytes(firstOffset,2,'little'))
            lengths=firstOffset
        while True:
            try:
                text = listScripts[i]
                text = str_to_bin(text,1)
                break
            except LookupError or IndexError: 
                print('i = %d, Offset= %s, text= %s'%(i,fp.tell(),texts[i-1]))
                exit()
        length = len(text)
        lengths+=length+1
        fp.seek(2,1)
    for i in range(numOfScripts):
        text=str_to_bin(listScripts[i],1)
        fp.write(text)
        fp.write(b'\x00')
    finishOffset=fp.tell()
    endOfFp=fp.seek(0,2)
    fp.seek(finishOffset,0)
    while fp.tell()!=endOfFp:
        fp.write(b'\x00')

def IDspsi_Import(fp,listScripts):

    IDspsi_SetOffset_im(fp,listScripts)




def find_dialog(textf):
    retlist=[]
    lines=textf.readlines()
    for line in lines:
        which=line.find(",")
        which2=line[which+1:].find(",")
        line=line[which+which2+2:].replace("\n","")
        retlist.append(line)
    return retlist

def dialog_num(headerList,data):
    dialogOffset=[]
    for i in headerList:
        dialogOffset.append(int.from_bytes(data[i+12:i+14],byteorder='little'))
    return dialogOffset

def find_header(find_str,data):
    count=0
    findOffset=[]
    where=data.find(find_str)
    findOffset.append(where)
    count+=1
    while True:
        where=data[findOffset[count-1]+4:].find(find_str)
        if where==-1 :
            break
        findOffset.append(where+4+findOffset[count-1])
        count+=1
    return findOffset

def str_to_bin(string_,sw):
    pathDir=os.getcwd()
    pathTbl=pathDir+'\\tbl.txt'
    tbl=open(pathTbl,'r',encoding='utf-16')
    kor=tbl.readline()
    jpn=tbl.readline()
    while True:
        try:
            if sw==1:                                               # Str to Bin : 입력기에서 사용
                string_=string_.replace('\n','&')
                string_=string_.translate(str.maketrans(
                    kor+'&①②③',
                    jpn+'＆１２３'))
                string_=bytes(string_,'shift-jis',errors='replace')#'ignore')
                string_=string_.replace(b'\x81\x95',b'\xff\x80')
                return string_
            elif sw==2:                                             # Bin to Str : 출력기에서 사용
                string_=string_.replace(b'\xFF\x80',b'\x81\x95')    # 개행을 전각&으로 출력
                string_=string_.replace(b'\xFF\x44',b'\x81\x83')    # 이하 < or >
                string_=string_.replace(b'\xFF\x42',b'\x81\x83')
                string_=string_.replace(b'\xFF\x40',b'\x81\x84')
                string_=string_.replace(b'\xFF\x00',b'\x81\x84')
                string_=str(string_,encoding='shift-jis',errors='replace')#'ignore')
                string_=string_.translate(str.maketrans(jpn,kor))
                string_=string_.replace('＆','\n')
                string_=string_.replace('&','\n')
                string_=string_.replace('+','…')

                return string_
        except UnicodeDecodeError or UnicodeEncodeError or LookupError as err:
            print("error: {0}".format(err))
            print('test')
            outerrlog=open('errLog.log','w')
            print(string_)
            outerrlog.write(string_)
            outerrlog.close()
            exit()

# 스크립트 추출기 8월5일 수정사항
#   이중배열로 추출함 dialog[0]에는 화자가 누군지, [1]에는 대사가 들어감
def script_extract(headerList,dialogNum,inf):
    count=0
    texts = ''
    dialogs=[[],[]]
    pathDir=os.getcwd()
    pathCsv =pathDir+ '\\오프셋별화자이름.xlsx'
    df=pd.read_excel(pathCsv,names=['None','offset','name'],index_col='offset')
    for h,d in zip(headerList,dialogNum):
        inf.seek(h)
        inf.seek(8,1)
        strangenum=inf.read(2)
        strangenum=int.from_bytes(bytes=strangenum,byteorder='little')   
        inf.seek(strangenum*16+6,1)
        lengths=0     
        inf.seek(16,1)
        
        dialogOffsets=[]
        speaker=[]
        for i in range(d):                  #대사 오프셋 리스트 작성
            name=speakerNameIntToStr(int.from_bytes(bytes=inf.read(2),byteorder='little'),df)
            dialogs[0].append(name)
            inf.seek(18,1)
            dialogOffsets.append(int.from_bytes(bytes=inf.read(2),byteorder='little'))
            inf.seek(10,1) 

        for i in range(d):                  #대사 리스트 작성. 대사 갯수만큼 반복
            inf.seek(h+dialogOffsets[i])    #대사 시작점으로 이동
            while True:
                try:
                    if d-1==i:              #else에서 행하는 i+1이 마지막에 d리스트의 범위를 초과함으로 예외처리
                        finishData=inf.read(100)
                        length=finishData.find(b'\x00')
                        text=finishData[0:length]
                    else:
                        length=dialogOffsets[i+1]-dialogOffsets[i]
                        text=inf.read(length)
                        length=text.find(b'\x00\x00')
                        if not length == -1:
                            text=text[0:length]
                        else: text=text[0:len(text)-1]

                    dialogs[1].append(text)
                    break
                except IndexError:
                    break
    #print(len(dialogs[1][1]))
    #print(dialogs[1][1])
    return dialogs

def script_import_gui(headerList,dialogNum,texts,inf):
    count=0
    finishOffset=0
    for h,d in zip(headerList,dialogNum):
        if inf.tell()==0:
            pass
        else:
            ETDFOffset=h
            num=ETDFOffset-finishOffset
            data=inf.read(num)
            pBinOffset=data.find(b'\x70\x42\x69\x6E')
            inf.seek(finishOffset)
            hex00appender(pBinOffset,inf)
        #Currentdata=data[h:]
        inf.seek(h)
        #print('Go to ETDF Offset')
        #print(inf.tell())
        inf.seek(8,1)
        strangenum=inf.read(2)
        strangenum=int.from_bytes(bytes=strangenum,byteorder='little')

        #Currentdata=Currentdata[strangenum*16+8:]
        inf.seek(strangenum*16+6,1)
        lengths=0
        #print('Go to dialogs length Offset')
        #print(inf.tell())
        inf.seek(36,1)
        for i in range(d):
            if i == 0: 
                firstOffset=int.from_bytes(bytes=inf.read(2),byteorder='little')
                #print(hex(firstOffset))
            else: 
                writeOffset=lengths
                inf.write(int.to_bytes(writeOffset,2,'little'))

            while True:
                try:
                    text=texts[count+i]
                    #text=str_to_bin(text,1)
                    break
                except LookupError or IndexError:
                    print('i = %d, d= %d, Offset= %s, text= %s'%(i,d,inf.tell(),texts[count+i-1]))
                    exit()
            length=len(text)
            if i==0:lengths=firstOffset+length+1
            else:lengths+=length+1
            inf.seek(30,1)
        
        inf.seek(-20,1)
        #print('Go to dialogs Offset')
        #print(inf.tell())
        for i in range(d):
            text=texts[count+i]
            while True:
                try:
                    #text=str_to_bin(text,1)
                    break
                except LookupError:
                    print(inf.tell())
                    print(text)
                    exit()
            inf.write(text)
            #print(inf.read(10))
            inf.write(b'\x00')
        finishOffset=inf.tell()
        count+=d
def hex00appender(num,outf):
    ff=b'\x00' # 추가 할 값
    i=0
    while i<num :
        outf.write(ff)
        i+=1

if __name__ == "__main__":
    main()