from tensorflow import keras
import os
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

test_dir = "chest_xray/test/"
model = keras.models.load_model('model_xray')
print(model.metrics)

