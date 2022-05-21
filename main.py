# Importing the necessary libraries
from flask import Flask, request, render_template, url_for
import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

# Loading pre-trained model
model = tf.keras.models.load_model('MNIST_ANN.h5')

# Creating an instance that will be our WSGI - Web Server Gateway Interface
# WSGI is a specification that describes how a web server communicates with web applications, 
# and how web applications can be chained together to process one request.
# __name__ tells flask to look for resources in templates and static folder
app = Flask(__name__)


# route() tells Flask what URL should trigger our function.
# Usually what we return is HTML
# A GET message is send, and the server returns data
@app.route('/', methods=['GET'])

def home():
    return render_template('index.html')

# POST method used to send HTML form data to the server. The data received by the POST method is not cached by the server.
@app.route('/', methods=['POST'])

def predict():
    # requesting the image file
    # name should match imagefile
    image_file = request.files['imagefile']

    # changing the filename to input.png
    image_file.filename = 'input.png'

    # defining the path to save the uploaded image
    image_path = './static/images/' + image_file.filename

    # saving the image
    image_file.save(image_path)

    # The input images vary in dimensions For example (256, 256, 3)
    # Input images consist of height, width, channels i.e 3 indicating RGB
    # Our model inputs b&w images as a numpy array of shape (28, 28) 
    img = img_to_array(load_img(image_path, target_size=(28, 28), color_mode="grayscale")) / 255.
    img = np.expand_dims(img, axis=0)

    # storing the model predictions on the given image
    result = model.predict(img)

    # passing variables prediction & confidence and rendering the HTML
    return render_template('index.html', prediction=np.argmax(result), confidence=round(np.max(result)*100, 2))


# runs the Flask python file
# debug=True hosts the web page in Debugging mode
# In Debugging Mode the server reloads automatically if any changes are made in the code
# You can also run the py file through cmd commands > set FLASK_APP=hello, > flask run 
# Flask locally hosts the app on default port 5000
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="localhost", port=8000, debug=True)
