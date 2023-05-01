
from PIL import Image

def toBinary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return binary

def encode():
    image = Image.open(input("Enter your image with extension: "), 'r')
    
    msg = input("Type in a message to encode: ")

    newImage = image.copy().convert('RGB')

    r, g, b = newImage.getpixel((1, 1))

    
    
def newPix():
    pass

def encodeMsg(img, msg):
    pass


encode()
    