import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, AveragePooling2D, Dense, BatchNormalization, Activation, GlobalAveragePooling2D, Concatenate, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

def conv_bn(x, filters, kernel_size, strides=1, padding='same', activation='relu'):
    x = Conv2D(filters, kernel_size, strides=strides, padding=padding, use_bias=False)(x)
    x = BatchNormalization()(x)
    if activation:
        x = Activation(activation)(x)
    return x

def inception_a(input):
    branch_1 = conv_bn(input, 96, 1)

    branch_2 = conv_bn(input, 64, 1)
    branch_2 = conv_bn(branch_2, 96, 3)

    branch_3 = conv_bn(input, 64, 1)
    branch_3 = conv_bn(branch_3, 96, 3)
    branch_3 = conv_bn(branch_3, 96, 3)

    branch_4 = AveragePooling2D(3, strides=1, padding='same')(input)
    branch_4 = conv_bn(branch_4, 96, 1)

    output = Concatenate()([branch_1, branch_2, branch_3, branch_4])
    return output

def reduction_a(input):
    branch_1 = conv_bn(input, 384, 3, strides=2, padding='valid')

    branch_2 = conv_bn(input, 192, 1)
    branch_2 = conv_bn(branch_2, 224, 3)
    branch_2 = conv_bn(branch_2, 256, 3, strides=2, padding='valid')

    branch_3 = MaxPooling2D(3, strides=2, padding='valid')(input)

    output = Concatenate()([branch_1, branch_2, branch_3])
    return output

# Repeat similar patterns for inception_b, inception_c, reduction_b

def InceptionV4(input_shape, num_classes):
    inputs = Input(input_shape)

    # Initial conv and pooling layers
    x = conv_bn(inputs, 32, 3, strides=2, padding='valid')
    x = conv_bn(x, 32, 3, padding='valid')
    x = conv_bn(x, 64, 3)
    x = MaxPooling2D(3, strides=2)(x)
    x = conv_bn(x, 80, 1, padding='valid')
    x = conv_bn(x, 192, 3, padding='valid')
    x = MaxPooling2D(3, strides=2)(x)

    # Multiple Inception-A blocks followed by a Reduction-A block
    for _ in range(4):
        x = inception_a(x)
    x = reduction_a(x)

    # Assume similar additions for B and C blocks with their reductions

    # Final pooling and dense layer for classification
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(1024, activation='relu')(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    return model

# Directory paths
base_dir = 'C:\\Users\\liorb\\git\\Final-Project\Data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical'
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical'
)

# Model configuration
model = InceptionV4(input_shape=(299, 299, 3), num_classes=1000)
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator,
    verbose=2  # Set to 2 for one line per epoch
)

# Print accuracy
train_acc = history.history['accuracy'][-1]
val_acc = history.history['val_accuracy'][-1]
print(f'Train Accuracy: {train_acc:.4f}')
print(f'Validation Accuracy: {val_acc:.4f}')

# Save the model
model.save('inception_v4_model.h5')
