from PIL import Image, ImageDraw, ImageFont

import math

char = "Wo- "[::-1]
charArray = list(char)
charLen = len(charArray)
interval = charLen/256

ScaleFactor = 0.3

charWidth = 8
charHeight = 18

def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]

text_file = open('output.txt', 'w') 

im = Image.open('Wall-E.jpg')

fnt = ImageFont.truetype("lucon.ttf", 15)

width, height = im.size

im = im.resize((int(ScaleFactor * width), int(ScaleFactor * height * 0.55)), Image.NEAREST)
width, height = im.size

pix = im.load()

outputImage = Image.new('RGB', (charWidth * width, charHeight * height), color=(0,0,0))
d = ImageDraw.Draw(outputImage)



for i in range(height):
    for j in range(width):
        
        r,g,b = pix[j,i]
        gray = int(r/3 + g/3 + b/3)
        pix[j,i] = (gray, gray, gray)
        text_file.write(getChar(gray))
        d.text((j*charWidth, i* charHeight),getChar(gray), font = fnt, fill = (r,g,b))
    
    text_file.write('\n')

outputImage.save('output.png')
