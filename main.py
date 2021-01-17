from keras.models import Model, load_model
from keras.applications import MobileNetV2
from keras.layers import Dense
from flask_cors import CORS, cross_origin
from flask import render_template, Flask, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import base64
import numpy as np
import cv2
import filters

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config["DEBUG"] = True
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

input_size = (224, 224, 3)


def get_model(input_shape=input_size, num_classes=2):
    # Load MobileNetV2
    mobilenet_model = MobileNetV2(input_shape=input_shape)
    # Bỏ đi layer cuối cùng (FC)
    mobilenet_model.layers.pop()
    # Đóng băng các layer (trừ 4 layer cuối)
    for layer in mobilenet_model.layers[:-4]:
        layer.trainable = False

    mobilenet_output = mobilenet_model.layers[-1].output

    # Tạo các layer mới

    output = Dense(num_classes, activation="softmax")
    # Lấy input từ output của MobileNet
    output = output(mobilenet_output)

    # Tạo model với input của MobileNet và output là lớp Dense vừa thêm
    model = Model(inputs=mobilenet_model.inputs, outputs=output)

    return model


# Thay đổi ảnh ở đây
def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64


def predict(fileName):
    # Đọc ảnh
    image_path = "uploads/" + fileName
    image = cv2.imread(image_path)
    # image_org = image.copy()

    # Chuyển đổi thành tensor
    image = cv2.resize(image, dsize=input_size[:2])
    image = image/255
    image = np.expand_dims(image, axis=0)

    # Tạo model
    model = get_model()

    # load the optimal weights
    model.load_weights("model/my_model.h5")

    # Tiến hành predict
    class_names = ['indoor','landscape']
    output = model.predict(image)
    class_name = class_names[np.argmax(output)]
    print("Hoang")
    # Nếu là landscape thì apply overlay
    if class_name == "landscape":
        filter_image = filters.apply_color_overlay(image, intensity=.2, red=250, green=100, blue=0)
        cv2.putText(filter_image,class_name,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imwrite("return/" + fileName, filter_image)
    else:
        # Nếu là indoor thì apply sepia
        filter_image = filters.apply_sepia(image, intensity=.8)
        cv2.putText(filter_image, class_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imwrite("return/" + fileName, filter_image)
    return fileName


@app.route('/')
def index():
    return render_template('page.html')


@app.route('/getfilter')
def getfilter():
    id = int(request.args.get('id'))
    if id == 0:
        # return predict(str(request.args.get('image')))
        # return 
        fileName = str(request.args.get('image'))
        image_path = "uploads/" + fileName
        image = cv2.imread(image_path)
        image_org = image.copy()

        # Chuyển đổi thành tensor
        image = cv2.resize(image, dsize=input_size[:2])
        image = image/255
        image = np.expand_dims(image, axis=0)

        # Tạo model
        model = get_model()

        # load the optimal weights
        model.load_weights("model/my_model.h5")

        # Tiến hành predict
        class_names = ['indoosr','indoor']
        output = model.predict(image)
        class_name = class_names[np.argmax(output)]

        # Nếu là landscape thì apply overlay
        if class_name == "indoosr":
            filter_image = filters.apply_color_overlay(image_org, intensity=.2, red=250, green=100, blue=0)
            cv2.putText(filter_image,class_name,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.imwrite("static/return/" + fileName, filter_image)
        else:
            # Nếu là indoor thì apply sepia
            filter_image = filters.apply_sepia(image_org, intensity=.8)
            cv2.putText(filter_image, class_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imwrite("static/return/" + fileName, filter_image)
        return fileName
    elif id == 1:
        return id   #Hamf filter 1
    elif id == 2:
        return id   #Viet 5 ham filter roi xu ly
    elif id == 3:
        return id   # -> luu lai cv2.imwrite("return/" + fileName, filter_image)
    elif id == 4:
        return id   # Nho return ve fileName
    elif id == 5:
        return id   #ok nha
    else:
        return False


@app.route('/upload', methods=['POST'])
def uploadImage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("kick phong",filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/", filename))
            return os.path.join(app.config['UPLOAD_FOLDER'] + '/' + filename)


if __name__ == "__main__":
    app.run()
