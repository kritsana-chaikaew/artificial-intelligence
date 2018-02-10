from keras.datasets import fashion_mnist
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU

from keras.models import load_model

(train_X, train_Y), (test_X, test_Y) = fashion_mnist.load_data()

classes = np.unique(train_Y)
nClasses = len(classes)

train_X = train_X.reshape(-1, 28, 28, 1)
test_X = test_X.reshape(-1, 28, 28, 1)

train_X = train_X.astype('float32')
test_X = test_X.astype('float32')

train_X = train_X / 255
test_X = test_X / 255

train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)

train_X, valid_X, train_label, valid_label = train_test_split(
        train_X, train_Y_one_hot, test_size=0.2, random_state=13)

batch_size = 64
epochs = 1
num_classes = 10

def build():
    model = Sequential()
    model.add(Conv2D(
            32,
            kernel_size=(3, 3),
            activation='linear',
            input_shape=(28, 28, 1),
            padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.25))

    model.add(Conv2D(
            64,
            kernel_size=(3, 3),
            activation='linear',
            padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.25))

    model.add(Conv2D(
            128,
            kernel_size=(3, 3),
            activation='linear',
            padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.4))

    model.add(Flatten())
    model.add(Dense(128, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(
            loss=keras.losses.categorical_crossentropy,
            optimizer=keras.optimizers.Adam(),
            metrics=['accuracy'])

    return model

def train(model):
    history = model.fit(
            train_X, train_label,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(valid_X, valid_label))

    return history

def evaluate(model, history):
    test_eval = model.evaluate(test_X, test_Y_one_hot, verbose=0)
    print('Test loss:', test_eval[0])
    print('Test accuracy:', test_eval[1])

    accuracy = history.history['acc']
    val_accuracy = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(accuracy))
    plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
    plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

#fashion_model = build()
#model_history = train(fashion_model)
#evaluate(fashion_model, model_history)

fashion_model = load_model('fashion_model_dropout.h5py')

predicted_classes = fashion_model.predict(test_X)
predicted_classes = np.argmax(np.round(predicted_classes), axis=1)
print(predicted_classes.shape, test_Y.shape)

correct = np.where(predicted_classes==test_Y)[0]
print('Found %d correct labels' % len(correct))
for i, correct in enumerate(correct[:9]):
   plt.subplot(3, 3, i+1)
   plt.imshow(test_X[correct].reshape(28, 28), cmap='gray', interpolation='none')
   plt.title("Predicted {}, Class {}".format(predicted_classes[correct], test_Y[correct]))
   plt.tight_layout()

plt.show()

incorrect = np.where(predicted_classes!=test_Y)[0]
print('Found %d incorrect labels' % len(incorrect))
for i, incorrect in enumerate(incorrect[:9]):
    plt.subplot(3, 3, i+1)
    plt.imshow(test_X[incorrect].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title('Predicted {}, Class {}'.format(predicted_classes[incorrect], test_Y[incorrect]))
    plt.tight_layout()

plt.show()
