from IPython import get_ipython
from IPython.display import display
# %%
# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.
import kagglehub
yudhaislamisulistya_plants_type_datasets_path = kagglehub.dataset_download('yudhaislamisulistya/plants-type-datasets')
keras_efficientnetv2_keras_efficientnetv2_b0_imagenet_2_path = kagglehub.model_download('keras/efficientnetv2/Keras/efficientnetv2_b0_imagenet/2')

print('Data source import complete.')

# %% [markdown]
# ![image.png](attachment:5f2e422d-a99f-4331-b29c-cabdae3f8715.png)
#
# *a picture from:*
# https://www.healthyforlifemeals.com/blog/beans-benefits-uses-and-more
#
# # Plants' Images Classificators with Tensorflow
# ### Plants, plants, a lot of plants everywhere
# In the real world, plants are indispensable to human life, providing essential resources that sustain and enhance our existence. From the food we eat to the air we breathe, plants play a crucial role in maintaining the delicate balance of our ecosystem.
#
# **Goal**
# The following notebook has been created for showing, how create a different models with tensorflow in few steps. There will be created 4 classificators (3 similar to the basic model described in Tensorflow guide but with some changes, and one pretrained model)
#
#
# **Dataset description**:
# The dataset contains 30,000 plants images, with 1,000 images per class and a diverse collection of 30 plant classes and 7 plant types, including crops, fruit, industrial, medicinal, nuts, tubers, and vegetable plants. The 30 plant classes include popular species such as banana, coconut, and pineapple, as well as lesser-known plants like bilimbi and galangal.
# %% [markdown]
# # Data preparation
#
# a first chapter includes:
#
# * libraries' import
# * dataset creation
#
# In the folder "plants-type-datasets" there are 30k plants' images splitted to 3 folders (train, test and validation). For our notebook all 3 folders will be joined and splitted randomly later. Therefore at the beginning there will be more additional steps for dataset preparation.
# %%
# libraries fo dataset preparation
import os
import random
import pandas as pd
import numpy as np
from IPython.display import Image

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# TensorFlow
import tensorflow as tf

# keras_cv for pretrained model usage
import keras_cv
# %%
# labels and images' paths preparation
dataset_root = '/kaggle/input/plants-type-datasets/split_ttv_dataset_type_of_plants'
labels = []
images_path = []

# Iterate through the subdirectories (plant categories)
for dataset in os.listdir(dataset_root):
    for plant_category in os.listdir(os.path.join(dataset_root, dataset)):
        if os.path.isdir(os.path.join(dataset_root, dataset, plant_category)):
            images = os.listdir(os.path.join(dataset_root, dataset, plant_category))

            # Create a data frame with image_path and label
            for image in images:
                image_path = os.path.join(dataset_root, dataset, plant_category, image)
                images_path.append(image_path)
                labels.append(plant_category)
# %%
# label and image's path veryfication
i = random.randint(0, 30000)
print(f'number of labels: {len(labels)} and images {len(images_path)}\n')
print('label of random plant: ', labels[i])
print('path to random image: ', images_path[i], '\n')
Image(images_path[i])
# %%
# general X and y preparation
X = images_path
y = labels
# %%
# One Hot Encoding for plants categories (y)
y = pd.get_dummies(y)
encoding_labels = y.columns
y=y.to_numpy()
# %%
# dataset splitting for train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1)

len(X_train), len(y_train), len(X_val), len(y_val), len(X_test), len(y_test)
# %% [markdown]
# # Preprocessing images
# ## (turning images into tensors)
# A few steps for changing images into numerical form and splitting they to smaller chunks (batches)
# %%
# parameters for image and batch size
img_size = 28
batch_size = 32
# %%
def prepare_image(image_path):
    '''
    turns an image into a tensor
    '''
    # read an image
    image = tf.io.read_file(image_path)
    # turn an image to numerical version
    image = tf.image.decode_jpeg(image, channels=3)
    # convert colours from 0-255 to 0-1
    image = tf.image.convert_image_dtype(image, tf.float32)
    # resize
    image = tf.image.resize(image, size=[img_size, img_size])

    return image
# %%
def get_label_image(image_path, label):
    image = prepare_image(image_path)

    return image, label
# %%
def create_batches(X, y=None, batch_size=batch_size, test_data=False):
    '''
    split a dataset to batches
    '''
    if test_data:
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
        data_batch = data.map(get_label_image).batch(batch_size)
    else:
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
        data = data.shuffle(buffer_size=len(X))
        data_batch = data.map(get_label_image).batch(batch_size)

    return data_batch
# %%
# batches creation for all datasets

# train data
train_data = create_batches(X_train, y_train)

# test data
test_data = create_batches(X_test, y_test, test_data=True)

# validation data
val_data = create_batches(X_val, y_val, test_data=True)
# %% [markdown]
# # Creation, training and validation of models
#
# In this chapter we will built and train following models:
# 1. basic model described in Tensorflow guide https://www.tensorflow.org/tutorials/keras/classification
# 2. basic model with modifications
# 3. basic model but trained longer (more epochs)
# 4. pretrained model from kaggle depository https://www.kaggle.com/models/keras/efficientnetv2
#
# The model 1 will be a basis for a comparison (reference point).
#
# To improve a model we can do for example:
# * extend dataset (in our case it is impossible)
# * add more layers to model (it will be tested in model 2)
# * train model longer (it will be done in model 3)
# * change the learning rate (again it will be tested in model 3)
# * use other model
# %%
# input and output shapes declaration
input_shape = [img_size, img_size, 3]
output_shape = len(encoding_labels)
# %% [markdown]
# ## Model 1
# %%
# model preparation
model_1 = tf.keras.Sequential([
    tf.keras.layers.Input(input_shape),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='softmax'),
    tf.keras.layers.Dense(output_shape)
])

model_1.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model_1.summary()
# %%
model_1.fit(train_data,
            epochs=5,
            validation_data=val_data,
            validation_freq=1,
           )
# %% [markdown]
# ## Model 2
#
# This model is an extended version of model 1.
#
# Differences between model 1 and model 2:
# * additional layer
# %%
# model preparation
model_2 = tf.keras.Sequential([
    tf.keras.layers.Input(input_shape),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='softmax'),
    tf.keras.layers.Dense(128, activation='softmax'),
    tf.keras.layers.Dense(output_shape)
])

model_2.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])
# %%
model_2.summary()
# %%
model_2.fit(train_data,
            epochs=5,
            validation_data=val_data,
            validation_freq=1,
           )
# %% [markdown]
# ## Model 3
#
# this model will be prepared as model 1 but during compilation the learning rate for the optimizer will be changed to 0.0005 and model 3 will be trained longer than model 1 and 2.
#
# %%
# model preparation
model_3 = tf.keras.Sequential([
    tf.keras.layers.Input(input_shape),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='softmax'),
    tf.keras.layers.Dense(output_shape)
])

model_3.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model_3.summary()
# %%
model_3.fit(train_data,
            epochs=10,
            validation_data=val_data,
            validation_freq=1,
           )
# %% [markdown]
# ## Model 4
# As a model 4 we will use one of the earlier trained model from kaggle repository: **EfficientNetV2**
#
# https://www.kaggle.com/models/keras/efficientnetv2
# %%
# define the model
model_4 = keras_cv.models.ImageClassifier.from_preset(
    "efficientnetv2_b0_imagenet",
    num_classes=output_shape
)
# %%
# compile the model
model_4.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer=tf.keras.optimizers.Adam(),
    metrics=['accuracy']
)

# build the model
model_4.build(input_shape)
# %%
model_4.summary()
# %%
# model training
model_4.fit(x=train_data,
            epochs=5,
            validation_data=val_data,
            validation_freq=1
         )
# %% [markdown]
# ## Predictions
# %%
# function for encoding labels
def pred_labels(prediction_propabilities):

    return encoding_labels[np.argmax(prediction_propabilities)]
# %%
# models verification on test data
models = [model_1, model_2, model_3, model_4]
index = random.randint(0, len(y_val))

for model in models:
    print(model)
    y_pred = model.predict(test_data)
    predictions = []
    test = []
    for i in range(len(y_pred)):
        predictions.append(pred_labels(y_pred[i]))
        test.append(pred_labels(y_test[i]))

    label = pred_labels(y_pred[index])
    print(f'Is {pred_labels(y_test[index])} predicted properly? Prediction: {label}. So:  {label==pred_labels(y_test[index])}')
    print('Accuracy for the whole test dataset: ', round(accuracy_score(test, predictions), 2), '\n--- ---\n')

print('\n\n')
print('Random plant\'s picture from test dataset which name models tried to predict')
Image(X_test[index])
# %% [markdown]
# # Summary
#
# There is not suprise that the pretrained model is the best. It was trained on the very big set of images earlier. 'Our' models were trained only on a small trained dataset. And as you can see the differences is huge. Basic model has accuracy <0.1, if we trained it longer with smaller learning rate we can achieve an accuracy 0.1 - 0.15, but the pretrained model can have accuracy bigger than 0.5 (eg 0.81) after 5 epochs! so, it is an incredible power of transfer learning.
#
# Thank you.
#
#  -the end-
#
# %% [markdown]
# Generar y descargar los modelos
# %%
# Guarda model_1
model_1.save('model_1_savedmodel.h5')

# Guarda model_2
model_2.save('model_2_savedmodel.h5')

# Guarda model_3
model_3.save('model_3_savedmodel.h5')

# Guarda model_4
model_4.save('model_4_savedmodel.h5')
# %%
print(encoding_labels)