import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

# Set random seed for reproducibility
np.random.seed(42)

# Define image directory
image_directory = 'datasets/'

# Load image paths for 'no' and 'yes' classes
no_tumor_images = [os.path.join(image_directory, 'no', filename) for filename in os.listdir(os.path.join(image_directory, 'no')) if filename.endswith('.jpg')]
yes_tumor_images = [os.path.join(image_directory, 'yes', filename) for filename in os.listdir(os.path.join(image_directory, 'yes')) if filename.endswith('.jpg')]

# Combine image paths and labels
image_paths = no_tumor_images + yes_tumor_images
labels = [0] * len(no_tumor_images) + [1] * len(yes_tumor_images)

# Shuffle and split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(image_paths, labels, test_size=0.2, random_state=42)

# Define image preprocessing function with data augmentation
def preprocess_image(image_path, input_size=(64, 64)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    image = cv2.resize(image, input_size)
    image = image / 255.0  # Normalize pixel values to [0, 1]
    return image

# Data augmentation
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

# Preprocess training and testing images
x_train = np.array([preprocess_image(image_path) for image_path in x_train])
x_test = np.array([preprocess_image(image_path) for image_path in x_test])

# Convert labels to categorical format
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

# Define the CNN model architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

# Compile the model
optimizer = Adam(lr=0.0001)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Train the model with data augmentation
model.fit_generator(train_datagen.flow(x_train, y_train, batch_size=32),
                    steps_per_epoch=len(x_train) / 32,
                    epochs=15,
                    validation_data=(x_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')

# Save the trained model
model.save('BrainTumor10Epochs.h5')
