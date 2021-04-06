import numpy as np
import random
from keras.utils import np_utils
import PIL.ImageOps
import os
from keras.preprocessing import image as image_utils
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, Dense
from flask import current_app
import time
from pathlib import Path

classes = []


def image_to_matrix(cate_list):
    if len(cate_list) == 0:
        raise Exception("No data to create data")
    config = current_app.config
    cate_ids = []
    for cate in cate_list:
        cate_ids.append(str(cate.cate_id))

    image_root = config['train_data_folder']
    train_data = []
    train_label = []
    classes_dir = os.listdir(image_root)
    unix_time = time.time() * 1000000
    num_label = 0
    for cls in classes_dir:
        if cls in cate_ids:
            cls_path = image_root + "/" + cls + "/"
            class_list = os.listdir(cls_path)
            num_label += 1
            for imageName in class_list:
                img_path = cls_path + imageName
                img = image_utils.load_img(img_path, target_size=(100, 100))
                # Invert Image
                img = PIL.ImageOps.invert(img)
                # convert img to array
                img = image_utils.img_to_array(img)
                train_data.append(img)
                train_label.append(int(cls))

    if len(train_data) > 0:
        train_data, train_label = shuffle(train_data, train_label)
        Path('np_train').mkdir(parents=True, exist_ok=True)
        data_path = f"np_train/{unix_time}_train_data.npy"
        label_path = f"np_train/{unix_time}_train_label.npy"
        np.save(data_path, np.array(train_data))
        np.save(label_path, np.array(train_label))

        return data_path, label_path, num_label
    else:
        raise Exception("No data to create data")


def shuffle(data, label):
    temp = list(zip(data, label))
    random.shuffle(temp)
    return zip(*temp)


def cnn_train(data_np_path, label_np_path, num_classes):
    np.random.seed(0)

    train_data = np.load(data_np_path)
    train_label = np.load(label_np_path)
    size = train_data.shape[1]

    # normalization
    train_data = train_data / 255.0

    train_data = train_data.reshape(train_data.shape[0], size, size, 3)

    # for example if label is 4 converts it [0,0,0,0,0]
    train_label = np_utils.to_categorical(train_label, num_classes)

    model = Sequential()

    # convolutional layer with 5x5 32 filters and with relu activation function
    # input_shape: shape of the each data
    # kernel_size: size of the filter
    # strides: default (0,0)
    # activation: activation function such as "relu","sigmoid"
    model.add(Conv2D(32, kernel_size=(1, 1), input_shape=(size, size, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    # beginning of fully connected neural network.
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.5))
    # Add fully connected layer with a softmax activation function
    model.add(Dense(num_classes, activation='softmax'))

    # Compile neural network
    model.compile(loss='categorical_crossentropy',  # Cross-entropy
                  optimizer='rmsprop',  # Root Mean Square Propagation
                  metrics=['accuracy'])  # Accuracy performance metric

    model.fit(train_data, train_label, epochs=20, verbose=1, batch_size=64)

    Path('modelsCNN').mkdir(parents=True, exist_ok=True)
    path = f"modelsCNN/{time.time() * 1000000}_hdf51.h5"
    model.save(path, overwrite=True, save_format="h5")
    return path


def predict_image_with_cnn(path, model_path="modelsCNN/hdf51.h5"):
    print(model_path)
    model = load_model(model_path)
    img = image_utils.load_img(path, target_size=(100, 100))  # open an image
    img = PIL.ImageOps.invert(img)  # inverts it
    img = image_utils.img_to_array(img)  # converts it to array
    img = img / 255.0
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])

    return model.predict_classes(img, verbose=0, batch_size=1)
