
from flask import Flask, render_template, request, redirect, url_for
from io import BytesIO
from PIL import Image

app = Flask(__name__)

#returns a string to it's binary equivalent list
def to_binary(msg):
    binary = [(format(ord(word), '08b')) for word in msg]
    return [*''.join(binary)]

#encodes an image given an image and message
def encode(img, msg):
    #to detect the end of a message
    msg += "@@@@@"

    new_image = img.copy().convert('RGB')

    #converting pixels and putting them into image copy
    new_image.putdata(encode_pix(new_image, to_binary(msg)))
    return new_image
    
#changes the LSB of the each rgb value in a pixel
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

#attempts to decode an image's data
def decode(img):
    msg = ''
    image_data = ''

    #cycles thorugh each pixel
    for pixel in list(img.convert('RGB').getdata()):
        
        #takes r, g, and b val from each pixel and extracts the LSB to add to the dataa
        r, g, b = tuple(pixel)
        r, g, b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
        image_data += '0' if r[-1] == '0' else '1'
        image_data += '0' if g[-1] == '0' else '1'
        image_data += '0' if b[-1] == '0' else '1'
    
    i = 0

    #loops through data until it reaches the stop (@@@@@) or the end
    while i < len(image_data):
        msg += chr(int(image_data[i:i+8], 2))
        if msg[-5:] == '@@@@@':
            break
        i += 8

    #returns message if stop is found, else says no message found
    if '@@@@@' in msg:    
        return msg[:-5]
    else:
        return "No decoded message was found."

#for terminal use, won't be helpful for website
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

#handles encoding form
@app.route('/encode', methods=['POST'])
def encode_img():
    image_byte = request.files['image']
    image = Image.open(BytesIO(image_byte.read()))
   
    msg = request.form['message']

    #encodes image and saves it
    encoded_image = encode(image, msg)
    encoded_image.save('static/images/encoded_image.png')

    return redirect(url_for('home'))

#handles decoding form
@app.route('/decode', methods=['POST'])
def decode_img():
    image_byte = request.files['image']
    image = Image.open(BytesIO(image_byte.read()))

    decoded_msg = decode(image)
    return decoded_msg

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
