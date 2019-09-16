#
# BDF font convertor
# coded by Nobu 15.Sep.2019
#

import sys
import math

class FontData:
    windowWidth = 0
    windowHeight = 0
    windowXoffset = 0
    windowYoffset = 0
    fontName = ""
    def __init__(self):
        self.bitmap = []
        self.width = 0
        self.height = 0
        self.xoffset = 0
        self.yoffset = 0
    def printElement(self):
        print("window width, height, xoffset, yoffset")
        print(str(self.windowWidth), str(self.windowHeight), str(self.windowXoffset),str(self.windowYoffset))
        print("font width, height, xoffset, yoffset")
        print(str(self.width), str(self.height), str(self.xoffset), str(self.yoffset))
class BdfFont(FontData):
    _strFontBoundingBox = "FONTBOUNDINGBOX"
    _strStartChar = "STARTCHAR"
    _strEndChar = "ENDCHAR"
    _strBitMap = "BITMAP"
    _strEncoding = "ENCODING"

    def __init__(self):
        self.strEncodingNumber = self._strEncoding + " "
        self.bitmap = []
        self.shiftedBitmap = []
        self.width = 0
        self.height = 0
        self.xoffset = 0
        self.yoffset = 0
        self.flagEncodeExist = False

    def setEncodingNumber(self, number):
        try:
            if number.startswith("0x"):
                self.intEncodingNumber = int(number, 16)
            else:
                self.intEncodingNumber = int(number)

        except ValueError:
            print("Invalid input number")
            exit()
        self.strEncodingNumber = self._strEncoding + " " + str(self.intEncodingNumber)
        #print(self.strEncodingNumber)

    def setFontFormatParameters(self, dataFile):
        for self.extractLine in dataFile:
            self.extractLine = self.extractLine.strip()
            if self.extractLine.startswith(self._strFontBoundingBox):
                self.tempFontBoundBox = self.extractLine
                break
        self.listFontBoundingBox = self.tempFontBoundBox.split()
        self.windowWidth = int(self.listFontBoundingBox[1])
        self.windowHeight = int(self.listFontBoundingBox[2])
        self.windowXoffset = int(self.listFontBoundingBox[3])
        self.windowYoffset = int(self.listFontBoundingBox[4])

    def setFontParameters(self, bbx):
        self.tempList = bbx.split()
        self.width = int(self.tempList[1])
        self.height = int(self.tempList[2])
        self.xoffset = int(self.tempList[3])
        self.yoffset = int(self.tempList[4])

    def bitmapArrayZeroClear(self):
        self.bitmapArray = []
        for self.m in range(self.windowHeight):
            self.tempList = []
            for self.n in range(self.windowWidth):
                self.tempList.append(0)
            self.bitmapArray.append(self.tempList)
        return self.bitmapArray

    def setShiftAmount(self):
        pass

    def bitmapList2Array (self, bitmapList):
        self.bitmap = []
        for self.m in range(len(bitmapList)):
            self.bitData = int(bitmapList[self.m], 16)
            self.temp = self.bitData
            self.tempList = []
            if self.width > 9:
                self.shiftBits = 16 - 1
            else:
                self.shiftBits = 8 - 1

            for self.n in range(self.width):
                self.bit = (1 << (self.shiftBits)) & self.temp
                self.temp = self.temp << 1
                if self.bit == (1 << (self.shiftBits)):
                    self.tempList.append(1)
                else:
                    self.tempList.append(0)
            self.bitmap.append(self.tempList)

    def printBitmap(self, charBitOne = "*", charBitZero = "-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for self.m in range(self.height):
            self.temp = ""
            for self.n in range(self.width):
                if self.bitmap[self.m][self.n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def printShiftedBitmap(self, charBitOne = "*", charBitZero = "-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for self.m in range(self.windowHeight):
            self.temp = ""
            for self.n in range(self.windowWidth):
                if self.shiftedBitmap[self.m][self.n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def getFontBitmap(self, dataFile, encoding):
        self.setEncodingNumber(encoding)
        self.extractedList = []
        self.flagFound = False
        self.flagNeverFound = True
        for self.extractLine in dataFile:
            self.extractLine = self.extractLine.strip()
            if self.extractLine == self.strEncodingNumber:
                self.flagFound = True
                self.flagNeverFound = False
            if self.extractLine == self._strEndChar:
                self.flagFound = False
            if self.flagFound:
                self.extractedList.append(self.extractLine)
        if not self.flagNeverFound:
            self.setFontParameters(self.extractedList[3])
            self.bitmapList2Array(self.extractedList[5:])
            self.flagEncodeExist = True
        else:
            self.bitmap = self.bitmapArrayZeroClear()
            self.flagEncodeExist = False
            #print(self.extractedList)

    def shiftBitmap(self):
        self.shiftedBitmap = self.bitmapArrayZeroClear()
        #print(self.shiftedBitmap)
        if not self.flagEncodeExist:
            return
        #print(self.shiftedBitmap)

        for self.m in range(self.windowHeight):
            for self.n in range(self.windowWidth):
                self.bitmap_x = self.n - self.xoffset + self.windowXoffset
                self.bitmap_y = self.m - self.yoffset + self.windowYoffset
                #print("bitX", self.bitmap_x.__str__(), ", bitY", self.bitmap_y.__str__())
                if self.bitmap_x >= 0 and self.bitmap_x < self.width:
                    if self.bitmap_y >= 0 and self.bitmap_y < self.height:
                        self.shiftedBitmap[self.m][self.n] = self.bitmap[self.bitmap_y][self.bitmap_x]

        #print(self.shiftedBitmap)




#### main body ###
if (len(sys.argv) == 2):
    filename = str(sys.argv[1])
    if (filename.endswith(".bdf")):
        with open(filename) as inputFontFile:
            dataFile = inputFontFile.readlines()
    else:
        print("Invalid inputfile")
        exit()
else:
    print("Invalid command input")
    exit()

#encodingNumber = input("Please input encoding number")
bdfFontData = BdfFont()
bdfFontData.setFontFormatParameters(dataFile)
#bdfFontData.printElement()
#bdfFontData.getFontBitmap(dataFile, encodingNumber)
#bdfFontData.printElement()
#bdfFontData.printBitmap()

bdfFontList = []
for m in range(0,10):
    #print("no. ", str(m))
    bdfFontData.getFontBitmap(dataFile, str(m).strip())
    print("{0:-^{width}s}".format("Code " + bdfFontData.intEncodingNumber.__str__(), width = bdfFontData.windowWidth + 8))
    print(str(bdfFontData.width), " ,", str(bdfFontData.height), " ,",  str(bdfFontData.xoffset),  " ,", str(bdfFontData.yoffset))
    bdfFontData.printBitmap("#", "-")
    bdfFontData.shiftBitmap()
    bdfFontData.printShiftedBitmap("*", ".")
    bdfFontList.append(bdfFontData.bitmap)

