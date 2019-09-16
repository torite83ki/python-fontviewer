import sys
import math

# fontviewer and converter


try:
    print("This is command argument : ", sys.argv[1])
except ValueError:
    print("No argument")
    exit()

if (len(sys.argv) == 2):
    filename = str(sys.argv[1])
    if (filename.endswith(".bdf")):
        with open(filename) as inputFontFile:
            dataFile = inputFontFile.readlines()
    else:
        exit()
else:
    exit()

encodingNumber = input("Please input encoding number")
try:
    if encodingNumber.startswith("0x"):
        intEncodingNumber = int(encodingNumber, 16)
    else:
        intEncodingNumber = int(encodingNumber)
except ValueError:
    print("Invalid Input")
    exit()

strSearchFontBaoundBox = "FONTBOUNDINGBOX"
strSearchWord = "ENCODING " + str(intEncodingNumber)
print(strSearchWord)

flagFound = False
extractedList = []
for extractLine in dataFile:
    extractLine = extractLine.strip()
    if extractLine.startswith(strSearchFontBaoundBox):
        strFontBoundBox = extractLine
    if strSearchWord == extractLine:
        flagFound = True
    if (flagFound and ("ENDCHAR" == extractLine)):
        flagFound = False

    if flagFound:
        extractedList.append(extractLine)

print(strFontBoundBox)
listFontBoundBox = strFontBoundBox.split()
print(listFontBoundBox)
intFontWidth = int(listFontBoundBox[1])
intFontHeight = int(listFontBoundBox[2])
intFontXoffset = int(listFontBoundBox[3])
intFontYoffset = int(listFontBoundBox[4])

print(extractedList)
bitmapList = extractedList[5:]

intlengthBitmap = len(bitmapList)
for n in range(len(bitmapList)):
    print("{0:0{width}b}".format(int(bitmapList[n], 16), width=intFontWidth))
    #print(str(int(bitmapList[n], 16)).zfill(intFontWidth))

outputLineList = []
for m in range(len(bitmapList)):
    bitData = int(bitmapList[m], 16)
    temp = bitData
    outputLineList = []
    for n in range(intFontWidth):
        bit = (1 << (intFontWidth - 1 )) & temp
        temp = temp << 1
        if bit == (1 << (intFontWidth - 1)):
            outputLineList.append("*")
        else:
            outputLineList.append("-")
    print(outputLineList)


def outputBitmap (bitmapList):
    for m in range(len(bitmapList)):
        bitData = int(bitmapList[m], 16)
        temp = bitData
        outputLineList = ""
        for n in range(intFontWidth):
            bit = (1 << (intFontWidth - 1 )) & temp
            temp = temp << 1
            if bit == (1 << (intFontWidth - 1)):
                outputLineList += "*"
            else:
                outputLineList += "-"
        print(outputLineList)


outputBitmap(bitmapList)

