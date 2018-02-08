from keras.datasets import fashion_mnist
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt

(train_X, train_Y), (test_X, test_Y) = fashion_mnist.load_data()
print('Trening data shape : ', train_X.shape, train_Y.shape)
print('Testin data shape : ', test_X.shape, test_Y.shape)

classes = np.unique(train_Y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

plt.figure(figsize=[5,5])

plt.subplot(121)
plt.imshow(train_X[0, :, :], cmap='gray')
plt.title('Ground Truth : {}'.format(train_Y[0]))

plt.subplot(122)
plt.imshow(test_X[0, :, :], cmap='gray')
plt.title('Ground Truth : {}'.format(train_Y[0]))
plt.show()
