
from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

def to_binary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return [*''.join(binary)]

def encode(img, msg):
    #to detect the end of a message
    msg += "@@@@@"

    new_image = img.copy().convert('RGB')

    new_image.putdata(encode_pix(new_image, to_binary(msg)))
    return new_image
    
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

def decode(img):
    msg = ''

    image_data = ''
    for pixel in list(img.getdata()):
        r, g, b = tuple(pixel)
        r, g, b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
        image_data += '0' if r[-1] == '0' else '1'
        image_data += '0' if g[-1] == '0' else '1'
        image_data += '0' if b[-1] == '0' else '1'
    
    i = 0
    while i < len(image_data):
        msg += chr(int(image_data[i:i+8], 2))
        if msg[-5:] == '@@@@@':
            break
        i += 8
    if '@@@@@' in msg:    
        return msg[:-5]
    else:
        return "No decoded message was found."

#for terminal use, won't be helpful for the actual website
def main():

    option = int(input("Enter 1 if you want to encode an image and 2 if you want to decode an image: "))

    if option == 1:
        encode()
    elif option == 2:
        decode()
    else:
        raise Exception("Not a valid option.")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode')
def encode_img():
    image = request.files['image']
    msg = request.form['message']
    encoded_image = encode(image, msg)
    return "Doanload the image here: <a href='/static/encoded_image.png'>Download</a>"



@app.route('/decode')
def decode_img():
    image = request.files['image']
    return decode(image)



if __name__ == '__main__':
    app.run(debug=True)

    