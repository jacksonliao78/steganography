
from PIL import Image

def to_binary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return [*''.join(binary)]

def encode():
    image = Image.open(input("Enter your image with extension: "), 'r')
    
    msg = input("Type in a message to encode: ") 
    msg += "@@@@@"

    new_image = image.copy().convert('RGB')

    r, g, b = new_image.getpixel((1, 1))

    new_image.putdata(encode_pix(new_image, to_binary(msg)))
    new_image_name = input("Enter the new image name with extension: ")
    new_image.save(new_image_name)
    
def encode_pix(img, msg):
    
    image_data = list(img.getdata())
    modified_data = []

    for i in range(len(msg) // 3 + 2):
        temp = list(image_data[i])
        for j in range(3):
            val = list(bin(image_data[i][j])[2:].zfill(8)) 
            if i*3 + j < len(msg) and val[-1] == '1' and msg[i*3 + j] == '0':
                val[-1] = '0'
            elif i*3 + j < len(msg) and val[-1] == '0' and msg[i*3 + j] == '1':
                val[-1] = '1'
            temp[j] = int(''.join(val), 2) 
        modified_data.append(tuple(temp))
    modified_data += image_data[len(modified_data):]        
    return modified_data

encode()
    