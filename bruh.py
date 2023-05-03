
from PIL import Image

def toBinary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return [*''.join(binary)]

def encode():
    image = Image.open(input("Enter your image with extension: "), 'r')
    
    msg = input("Type in a message to encode: ") 
    msg += "@@@@@"

    newImage = image.copy().convert('RGB')

    r, g, b = newImage.getpixel((1, 1))

    newImage.putdata(encodePix(newImage, toBinary(msg)))
    
def encodePix(img, msg):
    
    imageData = list(img.getdata())
    modifiedData = []

    for i in range(len(msg) // 3 + 2):
        temp = list(imageData[i])
        for j in range(3):
            val = list(bin(imageData[i][j])[2:].zfill(8)) 
            if i*3 + j < len(msg) and val[-1] == '1' and msg[i*3 + j] == '0':
                val[-1] = '0'
            elif i*3 + j < len(msg) and val[-1] == '0' and msg[i*3 + j] == '1':
                val[-1] = '1'
            temp[j] = int(''.join(val), 2) 
        modifiedData.append(tuple(temp))
    modifiedData += imageData[len(modifiedData):]        
    return modifiedData

encode()
    