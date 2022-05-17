from flask import Flask, request, render_template, url_for
import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

data = tf.keras.datasets.mnist.load_data()

model = tf.keras.models.load_model('MNIST_ANN.h5')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    image_file = request.files['imagefile']
    image_file.filename = 'input.png'
    image_path = './static/images/' + image_file.filename
    image_file.save(image_path)

    img = img_to_array(load_img(image_path, target_size=(28, 28), color_mode="grayscale")) / 255.
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    print(result)
    return render_template('index.html', prediction=np.argmax(result), confidence = np.max(result)*100, path = '.' + image_path)

if __name__ == '__main__':
    app.run(debug=True)