from PIL import Image

import math

char = "#Wo- "[::-1]
charArray = list(char)
charLen = len(charArray)
interval = charLen/256

ScaleFactor = 0.3

charWidth = 7
charHeight = 10

def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]

text_file = open('output.txt', 'w') 

im = Image.open('Wall-E.jpg')
width, height = im.size

im = im.resize((int(ScaleFactor * width), int(ScaleFactor * height)), Image.NEAREST)
width, height = im.size

pix = im.load()


for i in range(height):
    for j in range(width):
        
        r,g,b = pix[j,i]
        gray = int(r/3 + g/3 + b/3)
        pix[j,i] = (gray, gray, gray)
        text_file.write(getChar(gray))
    
    text_file.write('\n')

im.save('output.png')