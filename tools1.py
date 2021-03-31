# Authors: Samet Kalkan, Berk Gulay, Mert Surucuoglu

import numpy as np
import random
from keras.utils import np_utils
from PIL import Image
import cv2
import PIL.ImageOps
import os
from keras.preprocessing import image as image_utils

classes = ["No Rain", "Rainy"]


def binary_to_class(label):
	""" Converts a binary class matrix to class vector(integer)
		# Arguments:
			label: matrix to be converted to class vector
	"""
	new_lbl = []
	for i in range(len(label)):
		new_lbl.append(np.argmax(label[i]))
	return new_lbl


def get_accuracy_of_class(v_label, y):
	"""
		Returns:
			accuracy of given label
		Args:
			validation label: expected outputs
			y: predicted outputs
	"""
	c = 0
	for i in range(len(y)):
		if y[i] == v_label[i]:
			c += 1
	return c / len(y)


def separate_data(v_data, v_label):
	"""separates validation data and label according to class no
		Args:
			v_data: validation data to be split
			v_label: validation label to be split
		Returns:
			an array that stores '[val_data,val_label]' in each index for each class.
	"""
	vd = [[[], []] for _ in range(5)]
	for i in range(len(v_data)):
		cls = int(v_label[i])
		vd[cls][0].append(v_data[i])
		vd[cls][1].append(cls)
	for i in range(5):
		vd[i][0] = np.array(vd[i][0])
		vd[i][1] = np.array(vd[i][1])
	return vd


def __find_sky_area(path_of_image):
	read_image = cv2.imread(path_of_image, 50)
	edges = cv2.Canny(read_image, 150, 300)

	shape = np.shape(edges)
	left = np.sum(edges[0:shape[0] // 2, 0:shape[1] // 2])
	right = np.sum(edges[0:shape[0] // 2, shape[1] // 2:])

	if right > left:
		return 0  # if right side of image includes more building etc. return 0 to define left side(0 side) is sky area
	else:
		return 1  # if left side of image includes more building etc. return 1 to define right side(1 side) is sky area


def resize_image(base_size, path_of_image, destination, new_image_name):
	img = Image.open(path_of_image)

	if img.size[0] >= img.size[1]:
		sky_side = __find_sky_area(path_of_image)
		base_height = base_size
		wpercent = (base_height / float(img.size[1]))
		wsize = int((float(img.size[0]) * float(wpercent)))
		img = img.resize((wsize, base_height), Image.ANTIALIAS)
		if sky_side == 0:  # Left side is sky side, so keep it and crop right side
			img = img.crop((0, 0, base_size, img.size[1]))  # Keeps sky area in image, crops from other non-sky side
		else:  # Right side is sky side, so keep it and crop left side
			img = img.crop((img.size[0] - base_size, 0, img.size[0],
			                img.size[1]))  # Keeps sky area in image, crops from other non-sky side
		img.save(destination + '/' + new_image_name)
	else:
		base_width = base_size
		wpercent = (base_width / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		img = img.resize((base_width, hsize), Image.ANTIALIAS)
		img = img.crop((0, 0, img.size[0], base_size))  # Keeps sky area in image, crops from lower part
		img.save(destination + '/' + new_image_name)


def prepare_data_set(path, dest, size):
	# root directory for source images(which will be cropped)
	# path = '../train/1/'
	# root directory as destination to save cropped images(Prepared images will be saved in here)
	# dest = '../cropped100/1'

	for filename in os.listdir(path):
		resize_image(size,  # crop size for all images (just change it to define crop size)
		             path + filename,
		             dest,
		             filename)


def image_to_matrix(image_root):
	from keras.models import Sequential
	from keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, Dense

	train_data = []
	train_label = []

	classes_dir = os.listdir(image_root)

	for cls in classes_dir:
		class_list = os.listdir(image_root + cls + "/")  # image list in a class directory
		for imageName in class_list:
			print(imageName)
			img_path = image_root + cls + "/" + imageName
			img = image_utils.load_img(img_path, target_size=(100, 100))
			# Invert Image
			img = PIL.ImageOps.invert(img)
			# convert img to array
			img = image_utils.img_to_array(img)
			train_data.append(img)
			train_label.append(int(cls))

	if len(train_data) > 0:
		train_data, train_label = shuffle(train_data, train_label)
		np.save("train_data.npy", np.array(train_data))  # model root to save image models(image)
		np.save("train_label.npy", np.array(train_label))  # model root to save image models(label)
		# num_classes = 2
		# train_label = np_utils.to_categorical(train_label, num_classes)
		# model = Sequential()
		# size = train_data.shape[1]
		# train_data = train_data / 255.0
		# train_data = train_data.reshape(train_data.shape[0], size, size, 3)
		# model.add(Conv2D(32, kernel_size=(1, 1), input_shape=(size, size, 3), activation='relu'))
		# model.add(MaxPooling2D(pool_size=(2, 2)))
		# model.add(Conv2D(32, kernel_size=(5, 5), activation='relu'))
		# model.add(MaxPooling2D(pool_size=(2, 2)))
		#
		# model.add(Flatten())
		#
		# # beginning of fully connected neural network.
		# model.add(Dense(100, activation='relu'))
		# model.add(Dropout(0.5))
		# # Add fully connected layer with a softmax activation function
		# model.add(Dense(num_classes, activation='softmax'))
		#
		# # Compile neural network
		# model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
		#
		# # begin train the data
		# history = model.fit(train_data, train_label, epochs=20, verbose=2, batch_size=64)
		# model.save("modelsCNN/size100/test.h5", overwrite=False, save_format="h5")
		# model.save("modelsCNN/size100/test1.h5", overwrite=True, save_format="h5")
		# model.save("modelsCNN/size100/test.tf", overwrite=False, save_format="tf")
		# model.save("modelsCNN/size100/test1.tf", overwrite=True, save_format="tf")


def shuffle(data, label):
	temp = list(zip(data, label))
	random.shuffle(temp)
	return zip(*temp)


def concatenate():
	train_data = np.load("concat100/train_data8.npy")[:1000]
	train_label = np.load("concat100/train_label8.npy")[:1000]

	temp_data = np.load("concat100/train_data9.npy")[:1000]
	temp_label = np.load("concat100/train_label9.npy")[:1000]

	train_data = np.concatenate((train_data, temp_data), axis=0)
	train_label = np.concatenate((train_label, temp_label), axis=0)

	temp_data = np.load("concat100/train_data.npy")
	temp_label = np.load("concat100/train_label.npy")

	train_data = np.concatenate((train_data, temp_data), axis=0)
	train_label = np.concatenate((train_label, temp_label), axis=0)

	train_data, train_label = shuffle(train_data, train_label)
	np.save("concat100/train_data_concat1000.npy", train_data)
	np.save("concat100/train_label_concat1000.npy", train_label)


def split_data(train_data, train_label, ratio):
	x = int(len(train_data) * ratio)
	return train_data[x:], train_label[x:], train_data[:x], train_label[:x]


def split_and_save():
	train_data = np.load("concat100/train_data.npy", allow_pickle=True)
	train_label = np.load("concat100/train_label.npy", allow_pickle=True)

	train_data, train_label = shuffle(train_data, train_label)
	train_data, train_label, validation_data, validation_label = split_data(train_data, train_label, 0.25)

	np.save("concat100/train_data_n.npy", train_data)
	np.save("concat100/train_label_n.npy", train_label)
	np.save("concat100/validation_data.npy", validation_data)
	np.save("concat100/validation_label.npy", validation_label)


if __name__ == "__main__":
	image_to_matrix('dataset/')
# split_and_save()
