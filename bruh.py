
from PIL import Image

def toBinary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return binary

def encode():
    image = Image.open(input("Enter your image with extension: "), 'r')
    
    msg = input("Type in a message to encode: ")
    encodedImage = image.copy()

def encodeMsg(img, msg):
    pass


encode()
    