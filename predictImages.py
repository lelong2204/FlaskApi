import cv2
import ImageDescriptor as id
from keras.models import load_model
from keras.preprocessing import image as image_utils
from PIL import Image
import PIL.ImageOps
import tools as T


def predict_image_with_CNN(path, model):
	"""
		predicts an image
		Returns:
			path of the image and its class
	"""
	img = image_utils.load_img(path, target_size=(100, 100))  # open an image
	img = PIL.ImageOps.invert(img)  # inverts it
	img = image_utils.img_to_array(img)  # converts it to array
	img = img / 255.0
	img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])

	y = model.predict_classes(img, verbose=0, batch_size=1)
	return path, T.classes[y[0]]


def predict_image_with_RF(org_path, cropped_path, clf):
	"""
		predicts an image
		Returns:
			path of the image and its class
	"""
	feature = id.describe(org_path, cropped_path)
	y = clf.predict(feature)
	return (org_path, y[0])


hdf5 = load_model("modelsCNN/hdf51.h5")
# hdf5_1 = load_model("modelsCNN/hdf5_1.h5")
# tf = load_model("modelsCNN/tf1")
# tf_1 = load_model("modelsCNN/tf_1")
print("hdf5")
print(predict_image_with_CNN('img/hn-mua-2310.jpg', hdf5))
# print("hdf5_1")
# print(predict_image_with_CNN('img/6.jpg', hdf5_1))


# print("tf")
# print(predict_image_with_CNN('img/6.jpg', tf))
# print("tf_1")
# print(predict_image_with_CNN('img/6.jpg', tf_1))
