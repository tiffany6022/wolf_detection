# Import Keras libraries and packages
from tensorflow.keras.models import Sequential  # NN
from tensorflow.keras.layers import Conv2D  # Convolution Operation
from tensorflow.keras.layers import MaxPooling2D # Pooling
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense # Fully Connected Networks
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Input, Add, BatchNormalization, GlobalAveragePooling2D, Activation
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model

from keras.utils import np_utils

import numpy as np
import os
from sys import argv
from PIL import Image
import pickle

#! 多的?
# x_data = []
# y_data = []

#! function 命名盡量是個動詞
def build_input_data(data):
    count = 0
    x_data = []
    y_data = []
    dir_path = f'./division/episode2000/{data}'
    data_imgs = os.listdir(dir_path)
    for img_name in data_imgs:
        # x
        img_path = f'./division/episode2000/{data}/{img_name}'
        img_array = np.array(Image.open(img_path)) #(160, 160, 3)
        img_batch = np.expand_dims(img_array, axis=0) #(1, 160, 160, 3)
        if count == 0:
            x_data = img_batch
        else:
            x_data = np.concatenate((x_data, img_batch), axis=0)
        count += 1
        # y
        # wolf
        pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
        with open(pkl_path, 'rb') as file:
            df = pickle.load(file)
        date_mask = df['date'] == img_name[:4]
        if df[date_mask]['role'].isin(['wolf']).bool():
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


def identity_block(model, filter1, filter2, filter3):

    shortcut = model

    model = Conv2D(filter1, kernel_size=(1, 1), padding='same')(model)
    model = BatchNormalization(axis=3)(model)
    model = Activation('relu')(model)

    model = Conv2D(filter2, kernel_size=(3, 3), padding='same')(model)
    model = BatchNormalization(axis=3)(model)
    model = Activation('relu')(model)

    model = Conv2D(filter3, kernel_size=(1, 1), padding='same')(model)
    model = BatchNormalization(axis=3)(model)

    model = Add()([shortcut, model])
    model = Activation('relu')(model)

    return model

def conv_block(model, filter1, filter2, filter3):

    model = Conv2D(filter3, kernel_size=(1, 1), padding='same')(model)
    shortcut = BatchNormalization(axis=3)(model)

    model = Conv2D(filter1, kernel_size=(1, 1), padding='same')(model)
    model = BatchNormalization(axis=3)(model)
    model = Activation('relu')(model)

    model = Conv2D(filter2, kernel_size=(3, 3), padding='same')(model)
    model = BatchNormalization(axis=3)(model)
    model = Activation('relu')(model)

    model = Conv2D(filter3, kernel_size=(1, 1), padding='same')(model)
    model = BatchNormalization(axis=3)(model)

    model = Add()([shortcut, model])
    model = Activation('relu')(model)

    return model
def build_resnet():

    inputs = Input(shape=(115, 160, 3))

    model = Conv2D(64, kernel_size=(7, 7), padding='same')(inputs)
    model = BatchNormalization(axis=3)(model)
    model = Activation('relu')(model)
    model = MaxPooling2D()(model)

    model = conv_block(model, 64, 64, 256)
    model = identity_block(model, 64, 64, 256)
    model = identity_block(model, 64, 64, 256)

    model = conv_block(model, 128, 128, 512)
    model = identity_block(model, 128, 128, 512)
    model = identity_block(model, 128, 128, 512)

    # model = conv_block(model, 256, 256, 1024)
    # model = identity_block(model, 256, 256, 1024)
    # model = identity_block(model, 256, 256, 1024)
    # model = identity_block(model, 256, 256, 1024)
    #
    model = GlobalAveragePooling2D()(model)

    model = Dense(2, activation = 'softmax')(model)

    return Model(inputs, model)

def build_model():
    # initializing CNN
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', input_shape = (115, 160, 3), activation = 'relu')) # 128
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation = 'relu')) # 256
    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation = 'relu')) # 512
    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation = 'relu'))
    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation = 'relu'))
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

    # model = build_model()
    model = build_resnet()
    model.summary()
    optimizer = Adam(lr=0.0003)
    model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model_name = argv[1]
    tensorboard = TensorBoard(log_dir=f"./logs/episode2000/{model_name}", histogram_freq=0, write_graph=True, write_images=True)
    earlystopping = EarlyStopping(monitor='val_loss', patience=100, verbose=0, mode='auto')
    modelcheckpoint = ModelCheckpoint(f'./saved_models/episode2000/{model_name}', verbose=1, save_best_only=True)

    model.fit(x_train, y_train,
              batch_size=32,
              epochs=10,
              verbose=1,
              validation_data=(x_validation, y_validation),
              callbacks=[tensorboard, earlystopping, modelcheckpoint])
    score = model.evaluate(x_test, y_test, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

