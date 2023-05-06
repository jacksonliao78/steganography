
from PIL import Image

def to_binary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return [*''.join(binary)]

def encode():
    image = Image.open(input("Enter your image with extension: "), 'r')
    
    msg = input("Type in a message to encode: ") 
    #to detect the end of a message
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

        #creates a list of the rgb values for a pixel
        temp = list(image_data[i])
        for j in range(3):

            #r, g, or b val as a binary number to be modified
            val = list(bin(image_data[i][j])[2:].zfill(8)) 
            if i*3 + j < len(msg) and val[-1] == '1' and msg[i*3 + j] == '0':
                val[-1] = '0'
            elif i*3 + j < len(msg) and val[-1] == '0' and msg[i*3 + j] == '1':
                val[-1] = '1'
            
            #reassigning the rgb val, then appending the new pixel to modified_data
            temp[j] = int(''.join(val), 2) 
        modified_data.append(tuple(temp))
    
    #adding the unmodified data
    modified_data += image_data[len(modified_data):]        
    return modified_data

def decode():
    msg = ''
    image = Image.open(input("Enter your image with extension: "))
    print(list(image.getdata())[:10])

    image_data = ""
    for pixel in list(image.getdata())[:10]:
        r, g, b = tuple(pixel)
        r, g, b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
        image_data += '0' if r[-1] == '0' else '1'
        image_data += '0' if g[-1] == '0' else '1'
        image_data += '0' if b[-1] == '0' else '1'

    print(image_data)

    while True:
        pass

#encode()
decode()
    