# Import Keras libraries and packages
from tensorflow.keras.models import Sequential  # NN
from tensorflow.keras.layers import Conv2D  # Convolution Operation
from tensorflow.keras.layers import MaxPooling2D # Pooling
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense # Fully Connected Networks
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

from keras.utils import np_utils

import numpy as np
import os
from sys import argv
from PIL import Image

#! 多的?
# x_data = []
# y_data = []

#! function 命名盡量是個動詞
def build_input_data(data):
    count = 0
    x_data = []
    y_data = []
    dir_path = './division_crop/' + data
    data_imgs = os.listdir(dir_path)
    for img_name in data_imgs:
        # x
        img_path = './division_crop/' + data + '/' + img_name
        img_array = np.array(Image.open(img_path)) #(160, 160, 3)
        img_batch = np.expand_dims(img_array, axis=0) #(1, 160, 160, 3)
        if count == 0:
            x_data = img_batch
            print(x_data.shape)
        else:
            x_data = np.concatenate((x_data, img_batch), axis=0)
        count += 1
        # y
        if img_name[:4] == '0524' or img_name[:4] == '0531' or img_name[:4] == '0628' or img_name[:4] == '0719' or img_name[:4] == '0807'\
        or img_name[:4] == '0812' or img_name[:4] == '0815' or img_name[:4] == '0816' or img_name[:4] == '0925' or img_name[:4] == '1007'\
        or img_name[:4] == '0114' or img_name[:4] == '1213' or img_name[:4] == '0210' or img_name[:4] == '0120' or img_name[:4] == '0101':
            y_data.append(1)
        else:
            y_data.append(0)
    y_data = np.array(y_data)
    print(x_data.shape)
    print(y_data.shape)
    x_data = x_data.astype('float32')
    x_data = x_data / 255
    y_data = np_utils.to_categorical(y_data, 2)

    return (x_data, y_data)


def build_model():
    # initializing CNN
    model = Sequential()
    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', input_shape = (115, 160, 3), activation = 'relu')) # 128
    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(256, kernel_size=(3, 3), padding='same', activation = 'relu')) # 256
    model.add(Conv2D(256, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(512, kernel_size=(3, 3), padding='same', activation = 'relu')) # 512
    model.add(Conv2D(512, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(Conv2D(512, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(Conv2D(1024, kernel_size=(3, 3), padding='same', activation = 'relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    # model.add(Dense(4096, activation = 'relu'))
    model.add(Dense(512, activation = 'relu')) #512
    model.add(Dropout(0.6))
    model.add(Dense(2, activation = 'softmax'))

    return model

if "__main__" == __name__:
    (x_train, y_train) = build_input_data('train')
    (x_test, y_test) = build_input_data('test')
    (x_validation, y_validation) = build_input_data('validation')

    model = build_model()
    model.summary()
    optimizer = Adam(lr=0.0003)
    model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model_name = argv[1]
    tensorboard = TensorBoard(log_dir=f"./logs/{model_name}", histogram_freq=0, write_graph=True, write_images=True)
    earlystopping = EarlyStopping(monitor='val_loss', patience=300, verbose=0, mode='auto')
    modelcheckpoint = ModelCheckpoint(f'./saved_models/{model_name}', verbose=1, save_best_only=True)

    model.fit(x_train, y_train,
              batch_size=32,
              epochs=10,
              verbose=1,
              validation_data=(x_validation, y_validation),
              callbacks=[tensorboard, earlystopping, modelcheckpoint])
    score = model.evaluate(x_test, y_test, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

